BEGIN{
  OFS="\t"
  FS="\t"
}

{
  if (NF == 2) {
    mapping[$1] = $2;
  } if (mapping[$1] != "" && mapping[$3] != "") {
    print(mapping[$1], $2 ,mapping[$3])
  }
}

