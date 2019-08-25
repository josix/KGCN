BEGIN{
  OFS="\t"
  FS="\t"
}

{
  if (NF == 2) {
    mapping[$1] = $2;
  }
  if(NF > 2 && $1 != "\\N" && $2 != "\\N" && mapping[$1] != "" && mapping[$2] != "") {
    print(mapping[$1], "film.film.type",mapping[$2])
  }
  if(NF > 2 && $1 != "\\N" && $9 != "\\N" && mapping[$1] != "") {
    split($9,genres,",");
    for (i in genres){
      if (mapping[genres[i]] != ""){
        print(mapping[$1], "film.film.genre",mapping[genres[i]])
      }
    }
  }
}
