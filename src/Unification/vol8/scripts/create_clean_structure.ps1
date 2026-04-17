# create_clean_structure.ps1
# Creates clean series directory structure for Q, S, and G series.
# Does NOT delete anything. Only creates new folders.
# Run from vol5 root:
#   powershell -ExecutionPolicy Bypass -File scripts\create_clean_structure.ps1

$vol5 = Get-Location

function Make-Dir($path) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "  CREATED: $path"
    } else {
        Write-Host "  EXISTS:  $path"
    }
}

Write-Host ""
Write-Host "Creating clean series structure under: $vol5"
Write-Host "======================================================"

Write-Host ""
Write-Host "Q-Series (Quantum):"
Make-Dir "Q-Series\Q1_AtomicSpectra\lake"
Make-Dir "Q-Series\Q1_AtomicSpectra\scripts"
Make-Dir "Q-Series\NQ1_AtomicSpectra\lake"
Make-Dir "Q-Series\NQ1_AtomicSpectra\scripts"
Make-Dir "Q-Series\Q2_MolecularGeometry\lake"
Make-Dir "Q-Series\Q2_MolecularGeometry\scripts"
Make-Dir "Q-Series\NQ2_MolecularGeometry\lake"
Make-Dir "Q-Series\NQ2_MolecularGeometry\scripts"

Write-Host ""
Write-Host "S-Series (Stellar - Gaia Parallax):"
Make-Dir "S-Series\S1_GaiaParallax\lake"
Make-Dir "S-Series\S1_GaiaParallax\scripts"
Make-Dir "S-Series\NS1_GaiaParallax\lake"
Make-Dir "S-Series\NS1_GaiaParallax\scripts"

Write-Host ""
Write-Host "G-Series (Galactic - Galaxy Kinematics):"
Make-Dir "G-Series\G1_GalaxyKinematics\lake"
Make-Dir "G-Series\G1_GalaxyKinematics\scripts"
Make-Dir "G-Series\NG1_GalaxyKinematics\lake"
Make-Dir "G-Series\NG1_GalaxyKinematics\scripts"

Write-Host ""
Write-Host "======================================================"
Write-Host "MANUAL COPY STEPS REQUIRED:"
Write-Host ""
Write-Host "Q1 AtomicSpectra - copy raw lake:"
Write-Host "  copy Q-Series\Q1_Spectra\lake\q1_spectra_raw.jsonl Q-Series\Q1_AtomicSpectra\lake\q1_atomic_spectra_raw.jsonl"
Write-Host ""
Write-Host "Q2 MolecularGeometry - copy raw lake:"
Write-Host "  copy Q-Series\Q2_Molecular\lake\q2_molecular_raw.jsonl Q-Series\Q2_MolecularGeometry\lake\q2_molecular_geometry_raw.jsonl"
Write-Host ""
Write-Host "NQ2 MolecularGeometry - copy null raw lake:"
Write-Host "  copy Q-Series\NQ2_MolecularNull\lake\nq2_molecular_raw.jsonl Q-Series\NQ2_MolecularGeometry\lake\nq2_molecular_geometry_null_raw.jsonl"
Write-Host ""
Write-Host "S1 GaiaParallax - copy from NS6_7 (large file approx 357 MB):"
Write-Host "  copy S-Series\NS6_7\lake\Master_Stellar_Gaia_Standard.jsonl S-Series\S1_GaiaParallax\lake\s1_gaia_parallax_raw.jsonl"
Write-Host ""
Write-Host "G1 GalaxyKinematics - copy from NS6_7 (large file approx 1.5 GB):"
Write-Host "  copy S-Series\NS6_7\lake\Master_Galaxy_Vol6_Standard.jsonl G-Series\G1_GalaxyKinematics\lake\g1_galaxy_kinematics_raw.jsonl"
Write-Host ""
Write-Host "BUILD SCRIPTS - copy to series scripts folders:"
Write-Host "  copy scripts\build_q1_atomic_spectra_lake.py Q-Series\Q1_AtomicSpectra\scripts\"
Write-Host "  copy scripts\build_q2_molecular_geometry_lake.py Q-Series\Q2_MolecularGeometry\scripts\"
Write-Host "  copy scripts\build_s1_gaia_parallax_lake.py S-Series\S1_GaiaParallax\scripts\"
Write-Host "  copy scripts\build_g1_galaxy_kinematics_lake.py G-Series\G1_GalaxyKinematics\scripts\"
Write-Host ""
Write-Host "NS6_7 STATUS: Do NOT delete. Archive in place."
Write-Host "  It contains raw SDSS and Gaia data and audit scripts."
Write-Host ""
Write-Host "After copies complete, run Q1 and Q2 build scripts first."
Write-Host "Then S1 and G1 (large files, slow)."
Write-Host "======================================================"