<?php
header("Content-Type:text/html; charset=UTF-8");



$post_cust_card = $_POST['start'];




$array=array();

array_push($array,array(
	"flag"=> "0",
	"msg" => "this item is already in your cart"
	));
echo json_encode($array);








?>
