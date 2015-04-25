$files = Get-ChildItem -Filter *.md

for ($i=0; $i -lt $files.Count; $i++)
{
    $mdfile = $files[$i].Name
    $dir = "html/"
    $ext = ".html"
    $outfile = $dir + $mdfile + $ext

    Write-Host $outfile
    python html/md2html.py $mdfile -s $args -o $outfile
}
