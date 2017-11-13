editcap -D $numPack $inputPcap $outputPcap
tshark -Y "ip.dsfield == $priority" -r $outputPcap > $outputTxt
