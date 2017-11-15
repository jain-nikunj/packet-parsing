# Run this from the folder scripts/ inside the container, with your SSH keys ready
# The first argument is a reservation number
cd pcaps
rsync -a --include '*srn*/' --include 'tr0.pcap' --include 'Inputs/' --include 'batch_input.json' --include 'match_conf.json' --exclude '*' njain@sc2-lz:/share/nas/uc-berkeley/RESERVATION-$1/ $1
for f in $1/*/*.pcap; do editcap -D 3 $f ${f%.pcap}-edited.pcap; done
for f in $1/*/*-edited.pcap; do tshark -Y "ip.dsfield == 0x00" -r $f > ${f%.pcap}-leaky.txt; done
for f in $1/*/*-edited.pcap; do tshark -Y "ip.dsfield == 0x80" -r $f > ${f%.pcap}-high.txt; done
dest=$1
find $dest -type f | rename 's:(^|.*/)([^/]*)/([^/]*)$:${dest}/$2_$3:'
for f in $dest/*.txt; do mv $f "${f/uc-berkeley-test-scenario-/}"; done
cd ../
arr=(pcaps/$dest/*-high.txt)
for i in $(seq 0 ${#arr[@]}); do arr[$i]=${arr[$i]%high.txt}; done
mkdir images_$dest
for f in "${arr[@]}"; do python pcap2info.py 1 images_$dest ${f}leaky.txt ${f}high.txt; done
