#!/bin/bash
#
# Encrypt or Decrypt a file using GPG
#
# Input:
#   $1 - type: ENC or DEC
#   $2 - input file name to act upon
#   $3 - output file name
#

GPG='/usr/bin/gpg'
CIPHER=AES256

TYPE=${1}
INFILE=${2}
OUTFILE=${3}

usage() 
{

    echo "Usage: <ENC or DEC> Input-file Output-file"
    exit
}

[[ -z ${TYPE} || -z ${INFILE} || -z ${OUTFILE} ]] && \
    usage


if [ "${TYPE}" == 'ENC' ]
then
    $GPG -c --cipher-algo ${CIPHER} --output ${OUTFILE} ${INFILE}
    [ $? -ne 0 ] && { echo "Encryption failed!"; exit; }
    echo "Encryption succeded!" 
    # Want to delete the original plain text file?
    read -p "Do you want to delete the original ${INFILE}? (YES/no) " ANS
    [ "$ANS" == "YES" ] && { rm ${INFILE}; echo "${INFILE} deleted!"; }
     
elif [ "${TYPE}" == "DEC" ]
then
    $GPG --decrypt --output ${OUTFILE} ${INFILE}
    [ $? -ne 0 ] && { echo "Decryption failed!"; exit; }
    echo "Decryption succeded!, Please guard your plaintext file!!!" 
else 
    echo "Unknown action type!"
    usage
fi

echo "All Done, bye-bye!"



