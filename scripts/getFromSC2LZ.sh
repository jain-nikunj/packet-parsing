# Takes in a range of numbers, as well as a password
# Goes into the sc2 lz and searches it for the reservation files
# Within the given format. Assumes there exists a .ssh folder in the root
# of the user to define the sc2-lz path and a username

# read -s -p "SC2 LZ Password: " password 
ssh -t sc2-lz cd /share/nas/uc-berkeley ls
