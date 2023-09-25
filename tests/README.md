This directory contains data that can be used to test Belarusian orthography converters. Each CSV files starts with a header that describes what orthographies are present in the file. Each line is a separate test case. Example:

```csv
cyr_nar,cyr_taras,lat,comment
снег,сьнег,śnieh,мяккі знак
вуллі,вульлі,vulli,мяккі знак
```

The example above has test cases for Narkamauka <=> Taraskevica <=> Latin. The last column, comment, is an optional field. It's used to provide context of which feature test case verifies. 

Test cases can have empty values for certain orthographies.