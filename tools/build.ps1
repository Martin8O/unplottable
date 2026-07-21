<#
.SYNOPSIS
    Unplottable - build EPUB and A4 PDF from the manuscript (S5).

.DESCRIPTION
    Assembles manuscript/part-*/ into one book-shaped markdown file via
    `python tools\gate.py --assemble`, then runs pandoc over it.

    Front matter (title page, fan-work disclaimer, dedication, afterword) is
    E4's job; this build produces a readable draft artefact, not the release.

    Requirements, checked and reported before anything is attempted:
      * python  - always needed (assembly)
      * pandoc  - needed for both formats
      * a LaTeX engine (xelatex / lualatex / pdflatex / tectonic) - PDF only

.PARAMETER Format
    epub | pdf | both (default: both)

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
    [ValidateSet('epub', 'pdf', 'both')][string]$Format = 'both',
    [string]$OutDir = 'build',
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$title = 'Unplottable'
$stem = 'unplottable'

function Get-Tool([string]$name) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source } else { return $null }
}

Write-Host "== Unplottable build ==" -ForegroundColor Cyan
Write-Host "repo:   $repo"

$python = Get-Tool 'python'
$pandoc = Get-Tool 'pandoc'
$engines = @('xelatex', 'lualatex', 'pdflatex', 'tectonic')
$engine = $null
foreach ($e in $engines) { if (-not $engine -and (Get-Tool $e)) { $engine = $e } }

Write-Host "python: $(if ($python) { $python } else { 'NOT FOUND' })"
Write-Host "pandoc: $(if ($pandoc) { $pandoc } else { 'NOT FOUND' })"
Write-Host "pdf engine: $(if ($engine) { $engine } else { 'NOT FOUND' })"

if (-not $python) {
    Write-Host ""
    Write-Host "python not found - cannot assemble the manuscript." -ForegroundColor Red
    exit 3
}

if (-not $pandoc) {
    Write-Host ""
    Write-Host "pandoc not found - no EPUB or PDF can be built." -ForegroundColor Yellow
    Write-Host "  install:  winget install --id JohnMacFarlane.Pandoc"
    Write-Host "  then for PDF also a LaTeX engine, e.g.:"
    Write-Host "            winget install --id MiKTeX.MiKTeX"
    Write-Host "  (or build EPUB only: powershell tools\build.ps1 -Format epub)"
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
& $python (Join-Path $PSScriptRoot 'gate.py') --assemble $combined
if ($LASTEXITCODE -ne 0) { Write-Host "assembly failed." -ForegroundColor Red; exit $LASTEXITCODE }

$common = @(
    '--from', 'markdown+smart',
    '--standalone',
    '--toc', '--toc-depth=2',
    '--metadata', "title=$title",
    '--metadata', 'lang=en-GB'
)

$built = @()

if ($Format -in @('epub', 'both')) {
    $epub = Join-Path $out "$stem.epub"
    Write-Host "pandoc -> EPUB ..." -ForegroundColor Cyan
    & $pandoc $combined @common '--split-level=1' '--output' $epub
    if ($LASTEXITCODE -eq 0) { $built += $epub }
    else { Write-Host "EPUB build failed (exit $LASTEXITCODE)." -ForegroundColor Red }
}

if ($Format -in @('pdf', 'both')) {
    if (-not $engine) {
        Write-Host ""
        Write-Host "No LaTeX engine found - skipping PDF." -ForegroundColor Yellow
        Write-Host "  install:  winget install --id MiKTeX.MiKTeX   (then reopen the shell)"
    }
    else {
        $pdf = Join-Path $out "$stem.pdf"
        Write-Host "pandoc -> PDF (A4, $engine) ..." -ForegroundColor Cyan
        & $pandoc $combined @common `
            "--pdf-engine=$engine" `
            '-V' 'papersize=a4' `
            '-V' 'geometry:margin=2.5cm' `
            '-V' 'fontsize=11pt' `
            '-V' 'linkcolor=black' `
            '--output' $pdf
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
