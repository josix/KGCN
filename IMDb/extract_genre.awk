BEGIN{
  FS="\t"
  OFS="\t"
}
{
  if ($9 != "\\N"){
    split($9,genres,",");
    for (i in genres){
      print(genres[i]);
    }
  }
}
