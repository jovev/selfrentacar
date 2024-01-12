<?php
$ch = curl_init("https://cheapcarhire.rent/wp-json/my/price/getprice?date_from=3&date_to=5&from=1&to=5"); // such as http://example.com/example.xml
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HEADER, 0);
$data = curl_exec($ch);
print($data);
curl_close($ch);


?>