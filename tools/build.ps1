<#
.SYNOPSIS
    Unplottable - build EPUB, MOBI and A5 (book-size) PDF from the manuscript.

.DESCRIPTION
    Assembles manuscript/part-*/ into one book-shaped markdown file via
    `python tools\gate.py --assemble`, wraps it in the E4 front/back matter
    (book\00-front.md, book\99-afterword.md, book\metadata.yaml), and runs
    pandoc over the lot. MOBI is produced from the EPUB with Calibre's
    ebook-convert (no LaTeX needed for that leg).

    A cover image at book\cover.png (or .jpg) is embedded in EPUB + MOBI when
    present; the build works without one.

    Requirements, checked and reported before anything is attempted:
      * python        - always needed (assembly)
      * pandoc        - EPUB and PDF
      * ebook-convert - MOBI (ships with Calibre)
      * a LaTeX engine (xelatex / lualatex / pdflatex / tectonic) - PDF only

.PARAMETER Format
    epub | pdf | mobi | all (default: all)

.PARAMETER OutDir
    Output directory (default: build\ - gitignored)

.PARAMETER Check
    Only report tool availability, build nothing.

.EXAMPLE
    powershell tools\build.ps1
    powershell tools\build.ps1 -Format epub
    powershell tools\build.ps1 -Check
#>
[CmdletBinding()]
param(
    [ValidateSet('epub', 'pdf', 'mobi', 'all')][string]$Format = 'all',
    [string]$OutDir = 'build',
    [string]$Root = '',          # source root holding manuscript/ + book/ (default: repo, English). RU: 'Translation/RU'
    [string]$Stem = 'unplottable',
    [string]$Title = 'Unplottable',
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$srcRoot = if ($Root) { Join-Path $repo $Root } else { $repo }
$title = $Title
$stem = $Stem

function Get-Tool([string]$name) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source } else { return $null }
}

Write-Host "== Unplottable build ==" -ForegroundColor Cyan
Write-Host "repo:   $repo"

$python = Get-Tool 'python'
$pandoc = Get-Tool 'pandoc'
$calibre = Get-Tool 'ebook-convert'
if (-not $calibre) {
    $cal = Join-Path ${env:ProgramFiles} 'Calibre2\ebook-convert.exe'
    if (Test-Path $cal) { $calibre = $cal }
}
$engines = @('xelatex', 'lualatex', 'pdflatex', 'tectonic')
$engine = $null
foreach ($e in $engines) { if (-not $engine -and (Get-Tool $e)) { $engine = $e } }
# Self-contained tectonic on D: (see E4: MiKTeX ran C: out of space).
if (-not $engine -and (Test-Path 'D:\tools\tectonic\tectonic.exe')) {
    $engine = 'D:\tools\tectonic\tectonic.exe'
}
# Keep tectonic's TeX-bundle cache off C: (it defaults to %LOCALAPPDATA%).
if ($engine -like '*tectonic*' -and -not $env:TECTONIC_CACHE_DIR) {
    $env:TECTONIC_CACHE_DIR = 'D:\tools\tectonic\cache'
}

Write-Host "python:        $(if ($python) { $python } else { 'NOT FOUND' })"
Write-Host "pandoc:        $(if ($pandoc) { $pandoc } else { 'NOT FOUND' })"
Write-Host "ebook-convert: $(if ($calibre) { $calibre } else { 'NOT FOUND' })"
Write-Host "pdf engine:    $(if ($engine) { $engine } else { 'NOT FOUND' })"

if (-not $python) {
    Write-Host ""
    Write-Host "python not found - cannot assemble the manuscript." -ForegroundColor Red
    exit 3
}

$needPandoc = $Format -in @('epub', 'pdf', 'all') -or $Format -eq 'mobi'
if ($needPandoc -and -not $pandoc) {
    Write-Host ""
    Write-Host "pandoc not found - no EPUB/MOBI/PDF can be built." -ForegroundColor Yellow
    Write-Host "  install:  winget install --id JohnMacFarlane.Pandoc"
    Write-Host "  then for PDF also a LaTeX engine, e.g.:"
    Write-Host "            winget install --id MiKTeX.MiKTeX"
    Write-Host ""
    Write-Host "Nothing was built. The manuscript itself is unaffected." -ForegroundColor Yellow
    exit 3
}

if ($Check) { Write-Host ""; Write-Host "-Check: tooling reported, nothing built."; exit 0 }

$out = Join-Path $repo $OutDir
New-Item -ItemType Directory -Force -Path $out | Out-Null
$combined = Join-Path $out "$stem.md"

Write-Host ""
Write-Host "assembling ..." -ForegroundColor Cyan
& $python (Join-Path $PSScriptRoot 'gate.py') --assemble $combined --root $srcRoot
if ($LASTEXITCODE -ne 0) { Write-Host "assembly failed." -ForegroundColor Red; exit $LASTEXITCODE }

# --- E4 front/back matter + metadata + cover ------------------------------
$bookDir = Join-Path $srcRoot 'book'
$front = Join-Path $bookDir '00-front.md'
$after = Join-Path $bookDir '99-afterword.md'
$colophon = Join-Path $bookDir 'zz-colophon.md'
$meta = Join-Path $bookDir 'metadata.yaml'

$inputs = @()
if (Test-Path $front) { $inputs += $front }
$inputs += $combined
if (Test-Path $after) { $inputs += $after }
if (Test-Path $colophon) { $inputs += $colophon }

$cover = $null
foreach ($c in @('cover.png', 'cover.jpg', 'cover.jpeg')) {
    $p = Join-Path $bookDir $c
    if (-not $cover -and (Test-Path $p)) { $cover = $p }
}
Write-Host "cover:         $(if ($cover) { $cover } else { 'none (title page only)' })"

$common = @(
    '--from', 'markdown+smart',
    '--standalone',
    '--toc', '--toc-depth=1'
)
if (Test-Path $meta) { $common += @('--metadata-file', $meta) }
$common += @('--metadata', "title=$title", '--metadata', 'lang=en-GB')

$built = @()
$epub = Join-Path $out "$stem.epub"

if ($Format -in @('epub', 'mobi', 'all')) {
    Write-Host "pandoc -> EPUB ..." -ForegroundColor Cyan
    $epubArgs = @($inputs) + $common + @('--split-level=1')
    if ($cover) { $epubArgs += @("--epub-cover-image=$cover") }
    $epubArgs += @('--output', $epub)
    & $pandoc @epubArgs
    if ($LASTEXITCODE -eq 0) { $built += $epub }
    else { Write-Host "EPUB build failed (exit $LASTEXITCODE)." -ForegroundColor Red }
}

if ($Format -in @('mobi', 'all')) {
    if (-not (Test-Path $epub)) {
        Write-Host "no EPUB to convert - skipping MOBI." -ForegroundColor Yellow
    }
    elseif (-not $calibre) {
        Write-Host ""
        Write-Host "ebook-convert (Calibre) not found - skipping MOBI." -ForegroundColor Yellow
        Write-Host "  install Calibre from https://calibre-ebook.com/ (ebook-convert ships with it)"
    }
    else {
        $mobi = Join-Path $out "$stem.mobi"
        Write-Host "ebook-convert -> MOBI ..." -ForegroundColor Cyan
        & $calibre $epub $mobi --output-profile kindle
        if ($LASTEXITCODE -eq 0) { $built += $mobi }
        else { Write-Host "MOBI build failed (exit $LASTEXITCODE)." -ForegroundColor Red }
    }
}

if ($Format -in @('pdf', 'all')) {
    if (-not $engine) {
        Write-Host ""
        Write-Host "No LaTeX engine found - skipping PDF." -ForegroundColor Yellow
        Write-Host "  install:  winget install --id MiKTeX.MiKTeX   (then reopen the shell)"
    }
    else {
        $pdf = Join-Path $out "$stem.pdf"
        # A5 book block: the target is 300-400 printed pages (S6 rescale), which
        # this geometry delivers at roughly 300-330 words per page.
        Write-Host "pandoc -> PDF (A5 book, $engine) ..." -ForegroundColor Cyan
        # Palatino Linotype (body) + Consolas (mono) are on every Windows and
        # both cover Greek sigma - the manuscript's 3.61-sigma stats motif is
        # dropped by the default Latin Modern fonts, which have no Greek.
        $pdfArgs = @($inputs) + $common + @(
            "--pdf-engine=$engine",
            '-V', 'papersize=a5',
            '-V', 'geometry:margin=1.8cm',
            '-V', 'fontsize=10pt',
            '-V', 'linkcolor=black',
            '-V', 'mainfont=Palatino Linotype',
            '-V', 'monofont=Consolas',
            '-V', 'header-includes=\emergencystretch=3em',
            '--output', $pdf
        )
        & $pandoc @pdfArgs
        if ($LASTEXITCODE -eq 0) { $built += $pdf }
        else { Write-Host "PDF build failed (exit $LASTEXITCODE)." -ForegroundColor Red }
    }
}

Write-Host ""
if ($built.Count -eq 0) {
    Write-Host "Nothing was built." -ForegroundColor Yellow
    exit 3
}
Write-Host "built:" -ForegroundColor Green
foreach ($f in $built) {
    $kb = [math]::Round((Get-Item $f).Length / 1KB, 1)
    Write-Host ("  {0}  ({1} KB)" -f $f, $kb)
}
exit 0
