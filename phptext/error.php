<?php
$data['GET'] = $_GET;
$data['POST'] = $_POST;
$data['COOKIE'] = $_COOKIE;
foreach ($_SERVER as $k => $v) {
    if (preg_match("/^HTTP_/", $k)) {
        $k = substr($k, 5);
        $data['HEADER'][$k] = $v;
    }
}
echo json_encode($data);
?>

