#Create a simulator object
set ns [new Simulator]

$ns color 1 Blue
$ns color 2 Red
#Open the nam trace file
# TCP variant
set variant [lindex $argv 0]
# CBR rate
set rate [lindex $argv 1]

set nf [open ${variant}_output-${rate}.nam w]
$ns namtrace-all $nf

#Open the Trace file
set tf [open ${variant}_output-${rate}.tr w]
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
        #exec nam ${variant}_output-${rate}.nam &
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

#Creating a UDP agent and attach it to node n2
set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2
#Create a Null agent (a traffic sink) and attach it to node n3
set null3 [new Agent/Null]
$ns attach-agent $n3 $null3
$udp2 set fid_ 2
$udp2 set class_ 2

# Creating a CBR traffic source and attach it to udp2
set cbr2 [new Application/Traffic/CBR]

$cbr2 set type_ CBR
$cbr2 set packet_size_ 1000
$cbr2 set rate_ ${rate}mb
$cbr2 attach-agent $udp2
#Connect the traffic source with the traffic sink
$ns connect $udp2 $null3



if {$variant eq "Tahoe"} {
	set tcp [new Agent/TCP]
	$tcp set class_ 1	
	$ns attach-agent $n1 $tcp
	$tcp set fid_ 1
} elseif {$variant eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
	$tcp set class_ 1	
	$ns attach-agent $n1 $tcp
	$tcp set fid_ 1
} elseif {$variant eq "NewReno"} {
	set tcp [new Agent/TCP/Newreno]
	$tcp set class_ 1	
	$ns attach-agent $n1 $tcp
	$tcp set fid_ 1
} elseif {$variant eq "Vegas"} {
	set tcp [new Agent/TCP/Vegas]
	$tcp set class_ 1	
	$ns attach-agent $n1 $tcp
	$tcp set fid_ 1
} elseif {$variant eq "Cubic"} {
	set tcp [new Agent/TCP/Linux]
	$tcp set class_ 1	
	$ns attach-agent $n1 $tcp
	$tcp set fid_ 1
} 


#Setup a TCP connection

set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink


#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP
 

$ns at 0.1 "$cbr2 start"
$ns at 1.0 "$ftp start"
$ns at 8.0 "$ftp stop"
$ns at 9.0 "$cbr2 stop"
#Call the finish procedure after 5 seconds of simulation time
$ns at 10.0 "finish"
#Run the simulation
#Print CBR packet size and interval
puts "simulation for new reno"
puts "CBR packet size = [$cbr2 set packet_size_]"
puts "CBR interval = [$cbr2 set interval_]"

$ns run

