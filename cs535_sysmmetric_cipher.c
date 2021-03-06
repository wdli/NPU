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

/*****************************************
 * main
 ****************************************/

int main(void)
{

  char data[] = " Hello CS535B! ";

  char endata[1024];
  int enlen = 0;

  char dedata[1024];
  int  delen = 0;

  printf("Hello CS535 Symmetric Cipher \n");
  printf ("--------------------------------\n");

  memset(key,0,EVP_MAX_KEY_LENGTH);
  memset(iv,0,EVP_MAX_KEY_LENGTH);

  printf ("Select a key\n");
  CS535_select_random_key(key,KEY_LEN);

  printf ("Select a IV\n");
  CS535_select_random_iv(iv,KEY_LEN);

    
  memset(endata,0,sizeof(endata));
  memset(dedata,0,sizeof(endata));

 
  printf ("Start encryption data: %s\n", data);
  if(CS535_encrypt(data, strlen(data), endata, &enlen) < 0 ) {
    return;
  }
  printf (" Encrypted data length %d\n", enlen);
  
  printf ("Start decryption\n");
  if (CS535_decrypt(endata,enlen, dedata, &delen) < 0) {
    return;
  }
  printf (" Decrpted data: %s\n", dedata);
  printf (" Decrypted data length %d\n", delen);


  
  printf ("All Done!\n");
  printf ("--------------------------------\n");

  return;

}
