#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/rand.h>


/*
 * Globals
 */
static EVP_CIPHER_CTX ctx; // This has to be initialized once before encryption and once
                           // before decryption using the same key and IV

static unsigned char  key[EVP_MAX_KEY_LENGTH];
static unsigned char  iv[EVP_MAX_IV_LENGTH];

#define KEY_LEN 16 //bytes

#define CS535_EN_FILE "cs535_encrypted_file.txt"
#define CS535_DE_FILE "cs535_decrypted_file.txt"
#define CS535_KEY_FILE "cs535_encryption_key.txt"
#define CS535_IV_FILE "cs535_encryption_iv.txt"

#define MAX_BUF_LEN 1024
#define MAX_ENC_LEN 16

/*
 * select_random_key
 * 
 * len - key length in bytes
 */

static void
CS535_select_random_key(unsigned char *key, int len)
{
  int i;
  FILE* out = fopen(CS535_KEY_FILE,"wb");
  
  RAND_bytes(key,len);
  printf ("The key len is: %d bytes\n",len);
  for (i = 0; i < len; i++) {
    printf ("%02X ", key[i]);
  }
  fwrite(key,1,len,out);
  printf ("\n");

}

/*
 * select_random_iv
 * 
 * len - iv length in bytes
 */

static void
CS535_select_random_iv(unsigned char *iv, int len)
{
  int i;
  FILE* out = fopen(CS535_IV_FILE,"wb");
  
  RAND_bytes(iv,len);
  printf ("The iv len is: %d bytes\n",len);
  for (i = 0; i < len; i++) {
    printf ("%02X ", iv[i]);
  }
  fwrite(iv,1,len,out);
  printf ("\n");

}

/*
 * setup_for_encrption
 */
static int
CS535_setup_for_encryption(unsigned  char * key, unsigned char *iv)
{

  EVP_EncryptInit_ex(&ctx, EVP_aes_128_cbc(), NULL, key, iv);

  return 0;
}


/*
 * setup_for_decryption
 */
static int
CS535_setup_for_decryption(unsigned  char * key, unsigned char *iv)
{

  EVP_DecryptInit_ex(&ctx, EVP_aes_128_cbc(), NULL, key, iv);
  
  return 0;
}



/*
 * encryption
 *
 * Input: data - data to be encrypted
 *        data_len - data buffer length
 *   
 * Output: enbuf - buffer holds the encrypted data, 
 *
 */
static int
CS535_encrypt(unsigned char * data, int datalen, char *enbuf, int *enlen)
{

  int tmplen = 0;
  FILE * out;
  int rc;
  int i;

  printf (" Data len to be encrypted %d\n", datalen);
  CS535_setup_for_encryption(key, iv);

  if (!( rc = EVP_EncryptUpdate(&ctx, enbuf,enlen, data, datalen))) {
    printf (" Encrption error: %d\n",rc);
    return -1;
  }
  else {
    //
    // Final call: start at the end of the enbuf. The final may need
    // to add more padding after that point. The padding len is stored in tmplen
    //
    if (!( rc = EVP_EncryptFinal_ex(&ctx, enbuf+(*enlen), &tmplen))) {
      printf (" Finalization error: %d\n", rc);
      return -1;
    }
  }
  printf (" The enlen = %d, final tmplen = %d\n",*enlen, tmplen);
  *enlen += tmplen;

  out = fopen(CS535_EN_FILE,"wb");

  fwrite(enbuf,1,*enlen, out);
  printf (" Encrypted data saved to file: %s\n", CS535_EN_FILE);
  printf ("\n");

  return 0;
}



/*
 * CS535_encrypt2
 *
 * Input: data - data to be encrypted
 *        data_len - data buffer length
 *        Note: key, IV and CTX are globally-accessible
 *
 * Output: enbuf - buffer holds the encrypted data, 
 *
 */
static int
CS535_encrypt2(unsigned char * data, int datalen, char *enbuf, int *enlen)
{

  int tmplen = 0;
  FILE * out;
  int rc;
  int i;
  int ol = 0; // moving index to keep track of encryption progress
  printf ("--------------------------------------------------\n");
  printf ("Original Data len to be encrypted %d\n", datalen);

  /*  set up the encryption context*/
  CS535_setup_for_encryption(key, iv);

  /* check the output data buffer len */
  if ( (datalen + EVP_CIPHER_CTX_block_size(&ctx)) > MAX_BUF_LEN ) {
    printf (" Output buffer len is too small!\n");
    return -1;
  }

  /* start encryption MAX_ENC_LEN at a time*/
  for ( i=0; i <= datalen/MAX_ENC_LEN; i++) {
    if (!( rc = EVP_EncryptUpdate(&ctx, &enbuf[ol], &tmplen, &data[ol], MAX_ENC_LEN))) {
      printf (" Encrption error: %d\n",rc);
      return -1;
    }    
    ol += tmplen;
    printf ("Encrypted %d bytes, total len %d\n", tmplen, ol);
  }

  /* Encrypt the last residue length*/
  if (datalen % MAX_ENC_LEN) {
    if (!( rc = EVP_EncryptUpdate(&ctx, &enbuf[ol], &tmplen, &data[ol], datalen % MAX_ENC_LEN))) {
      printf (" Encrption error at the end: %d\n",rc);
      return -1;
    }    
    ol += tmplen;
    printf ("Encrypted %d bytes at the end, total len %d\n", tmplen, ol);    
  }

  
  /* Finalize */
  if (!( rc = EVP_EncryptFinal_ex(&ctx, &enbuf[ol], &tmplen))) {
      printf (" Finalization error: %d\n", rc);
      return -1;
  }  
  ol += tmplen;
  *enlen = ol;

  printf (" Finalize len    = %d\n", tmplen);
  printf (" Final total len = %d\n", ol);
  
  out = fopen(CS535_EN_FILE,"wb");

  fwrite(enbuf,1,*enlen, out);
  printf (" Encrypted data saved to file: %s\n", CS535_EN_FILE);
  printf ("\n");

  return 0;
}


/*
 * CS535_decrypt
 */
static int
CS535_decrypt(char* data, int datalen, char *debuf, int *delen)
{


  int tmplen = 0;
  FILE * out;
  int rc;


  printf (" Data len to be decrypted %d\n", datalen);

  CS535_setup_for_decryption(key,iv);
  if (!( rc = EVP_DecryptUpdate(&ctx, debuf, delen, data, datalen))) {
    printf (" Decryption error: %d\n", rc);
    return -1;
  }
  printf (" DecryptUpdate delen = %d \n", *delen);

  printf (" Finalizing... \n");
  if ((rc = EVP_DecryptFinal_ex(&ctx, debuf, &tmplen)) == 0) {
    printf (" Finalization error: %d\n", rc);
    return -1;
  }
  printf (" DecryptFinal tmplen = %d\n",tmplen);
  *delen += tmplen;
  
  debuf[*delen] = '\0';
  
  out = fopen(CS535_DE_FILE,"wb");
  fwrite(debuf,1, *delen, out);
  printf (" Decrypted data saved to file: %s\n", CS535_DE_FILE);
  return 0;  

}

/*
 * CS535_decrypt2
 */
static int
CS535_decrypt2(char* data, int datalen, char *debuf, int *delen)
{
  int rc;
  int tmplen;

  printf("Data len before decryption: %d\n",datalen);

  CS535_setup_for_decryption(key,iv);
  if (datalen + EVP_CIPHER_CTX_block_size(&ctx) + 1 > MAX_BUF_LEN) {
    printf (" Buffer too small for decryption\n");
    return -1;
  }

  EVP_DecryptUpdate(&ctx, debuf, delen, data, datalen);
  if (!*delen) {
    printf(" Decryption len is zero!");
    return -1;
  }
  printf(" Total decrypted len before final = %d\n", *delen);

  /*
  if ((rc = EVP_DecryptFinal_ex(&ctx, debuf, &tmplen)) == 0) {
    printf (" Finalization error: %d\n", rc);
    return -1;
  }

  *delen += tmplen;
  */
  debuf[*delen] = '\0';
  printf(" Total decrypted len after final = %d\n", *delen);

  return 0;

}

/*****************************************
 * main
 ****************************************/

int main(int argc, char *argv[])
{

  // char data[] = " Hello CS535B! ";
  if (!argv[1]) {
    printf ("Missing string to be encrypted!\n");
    return;
  }

  char *data = strdup(argv[1]);

  char endata[MAX_BUF_LEN];
  int enlen = 0;

  char dedata[MAX_BUF_LEN];
  int  delen = 0;

  printf("Hello CS535 Symmetric Cipher Exercise! \n");
  printf ("String to be encrypted: %s\n", data );
  printf ("--------------------------------\n");

  /* select key and IV*/
  memset(key,0,EVP_MAX_KEY_LENGTH);
  memset(iv,0,EVP_MAX_KEY_LENGTH);

  printf ("Selecting a key\n");
  CS535_select_random_key(key,KEY_LEN);

  printf ("Selecting an IV\n");
  CS535_select_random_iv(iv,KEY_LEN);

    
  memset(endata,0,sizeof(endata));
  memset(dedata,0,sizeof(endata));

  /* Encryption */
  printf ("Start encrypting data: %s\n", data);
  if(CS535_encrypt2(data, strlen(data), endata, &enlen) < 0 ) {
    return;
  }
  printf (" Encrypted data length %d\n", enlen);
  
  /* Ask if continue to decryption */
  char ans[10];
  memset(ans,0,10);
  printf ("Do you want to continue (yes/no)?\n");
  scanf("%s", ans);
  printf ("Ans is %s\n",ans);
  if (strcmp(ans,"yes") != 0 ){
    printf ("Bye bye!\n");
    return;
  }
  
  printf ("--------------------------\n");
  
  printf ("Start decrypting\n");
  if (CS535_decrypt2(endata,enlen, dedata, &delen) < 0) {
    return;
  }
  printf (" Decrpted data: %s\n", dedata);
  printf (" Decrypted data length %d\n", delen);


  
  printf ("All Done!\n");
  printf ("--------------------------------\n");

  return;

}
