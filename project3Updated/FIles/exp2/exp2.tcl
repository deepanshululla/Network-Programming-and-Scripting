#Create a simulator object
set ns [new Simulator]

$ns color 1 Blue
$ns color 2 Red
$ns color 3 Green
# TCP var1
set var1 [lindex $argv 0]
set var2 [lindex $argv 1]
# CBR rate
set rate [lindex $argv 2]

#Open the nam trace file
set nf [open out.nam w]
$ns namtrace-all $nf

#Open the Trace file
set tf [open ${var1}_${var2}_output-${rate}.tr w]
$ns trace-all $tf



#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Close the Trace file
        close $tf
        #Execute NAM on the trace file
        #exec nam out.nam &
        exit 0
}

#Create six nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create a duplex link between the nodes
#Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail


$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n6 $n3 10Mb 10ms DropTail


#Give node position (for NAM)
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n6 orient right-down

#Monitor the queue for link (n2-n3). (for NAM)
$ns duplex-link-op $n2 $n3 queuePos 0.5

#Create a UDP agent and attach it to node n1
set udp [new Agent/UDP]
$udp set class_ 3
$ns attach-agent $n2 $udp
#Create a Null agent (a traffic sink) and attach it to node n3
set null [new Agent/Null]
$ns attach-agent $n3 $null
$udp set fid_ 3

# Create a CBR traffic source and attach it to udp0
set cbr [new Application/Traffic/CBR]
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ ${rate}mb
$cbr set random_ false
$cbr attach-agent $udp



#Connect the traffic source with the traffic sink
$ns connect $udp $null

#Setup a TCP connection
#Setup a TCP conncection
if {($var1 eq "Reno")} {
	set tcp1 [new Agent/TCP/Reno]
	$tcp1 set class_ 1
	$ns attach-agent $n1 $tcp1
	$tcp1 set fid_ 1
} elseif {($var1 eq "NewReno")} {
	set tcp1 [new Agent/TCP/Newreno]
	$tcp1 set class_ 1
	$ns attach-agent $n1 $tcp1
	$tcp1 set fid_ 1	
} elseif {($var1 eq "Vegas")} {
	set tcp1 [new Agent/TCP/Vegas]
	$tcp1 set class_ 1
	$ns attach-agent $n1 $tcp1
	$tcp1 set fid_ 1
} elseif {($var1 eq "Cubic")} {
	set tcp1 [new Agent/TCP/Linux]
	$tcp1 set class_ 1
	$ns attach-agent $n1 $tcp1
	$tcp1 set fid_ 1
}



set sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1


$ns connect $tcp1 $sink1


#Setup a FTP over TCP connection
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP

if {($var2 eq "Reno")} {
	set tcp2 [new Agent/TCP/Reno]
	$tcp2 set class_ 2
	$ns attach-agent $n5 $tcp2
} elseif {($var2 eq "NewReno")} {
	set tcp2 [new Agent/TCP/Newreno]
	$tcp2 set class_ 2
	$ns attach-agent $n5 $tcp2
} elseif {($var2 eq "Vegas")} {
	set tcp2 [new Agent/TCP/Vegas]
	$tcp2 set class_ 2
	$ns attach-agent $n5 $tcp2
} elseif {($var2 eq "Cubic")} {
	set tcp2 [new Agent/TCP/Linux]
	$tcp2 set class_ 2
	$ns attach-agent $n5 $tcp2
}



set sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $sink2
$ns connect $tcp2 $sink2
$tcp2 set fid_ 2

#Setup a FTP over TCP connection
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP
 


$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp1 start"
$ns at 1.0 "$ftp2 start"
$ns at 9.0 "$ftp2 stop"
$ns at 9.0 "$ftp1 stop"
$ns at 9.5 "$cbr stop"

#Call the finish procedure after 5 seconds of simulation time
$ns at 10.0 "finish"
#Run the simulation
#Print CBR packet size and interval
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"
$ns run

