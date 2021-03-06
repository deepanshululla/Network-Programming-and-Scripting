#Create a simulator object
set ns [new Simulator]

$ns color 1 Blue
$ns color 2 Red
#Open the nam trace file
# TCP var
set tcp_var [lindex $argv 0]
# Queue var
set q_var [lindex $argv 1]

set nf [open ${tcp_var}-${q_var}_output.nam w]
$ns namtrace-all $nf

#Open the Trace file
set tf [open ${tcp_var}-${q_var}_output.tr w]
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
        #exec nam ${tcp_var}-${q_var}_output.nam &
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
#create links between the nodes
if {$q_var eq "DropTail"} {
	$ns duplex-link $n1 $n2 10Mb 10ms DropTail
	$ns duplex-link $n2 $n3 10Mb 10ms DropTail
	$ns duplex-link $n5 $n2 10Mb 10ms DropTail
	$ns duplex-link $n4 $n3 10Mb 10ms DropTail
	$ns duplex-link $n6 $n3 10Mb 10ms DropTail
} elseif {$q_var eq "RED"} {
	$ns duplex-link $n1 $n2 10Mb 10ms RED
	$ns duplex-link $n2 $n3 10Mb 10ms RED
	$ns duplex-link $n5 $n2 10Mb 10ms RED
	$ns duplex-link $n4 $n3 10Mb 10ms RED
	$ns duplex-link $n6 $n3 10Mb 10ms RED
}


#Give node position (for NAM)
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n6 orient right-down

#Monitor the queue for link (n2-n3). (for NAM)
$ns duplex-link-op $n2 $n3 queuePos 0.5

$ns queue-limit	$n1 $n2 10
$ns queue-limit	$n5 $n2 10
$ns queue-limit	$n2 $n3 10
$ns queue-limit	$n4 $n3 10
$ns queue-limit	$n6 $n3 10

#Creating a UDP agent and attach it to node n2
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
#Create a Null agent (a traffic sink) and attach it to node n3
set null [new Agent/Null]
$ns attach-agent $n6 $null
$udp set fid_ 2
$udp set class_ 2

# Creating a CBR traffic source and attach it to udp2
set cbr [new Application/Traffic/CBR]

$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 7mb
$cbr attach-agent $udp
#Connect the traffic source with the traffic sink
$ns connect $udp $null

#Setup a TCP connection
if {$tcp_var eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
	set sink [new Agent/TCPSink]
} elseif {$tcp_var eq "SACK"} {
	set tcp [new Agent/TCP/Sack1]
	set sink [new Agent/TCPSink/Sack1]
} elseif {$tcp_var eq "Cubic"} {
	set tcp [new Agent/TCP/Linux]
	set sink [new Agent/TCPSink]
}


$tcp set class_ 1
$ns attach-agent $n1 $tcp

$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP
 

$ns at 0.1 "$ftp start"
$ns at 3.0 "$cbr start"
$ns at 9.0 "$ftp stop"
$ns at 9.5 "$cbr stop"
#Call the finish procedure after 5 seconds of simulation time
$ns at 10.0 "finish"
#Run the simulation
#Print CBR packet size and interval



$ns run

