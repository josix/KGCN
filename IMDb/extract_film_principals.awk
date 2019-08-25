BEGIN{
  OFS="\t"
  FS="\t"
}

{
  if (NF == 2) {
    mapping[$1] = $2;
  } else if($1 != "\\N" && $4 != "\\N" && $3 != "\\N" && mapping[$1] != "" && mapping[$3] != "") {
    print(mapping[$1], "film.film."$4,mapping[$3])
  }
}
