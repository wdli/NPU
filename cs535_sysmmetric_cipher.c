#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/rand.h>


/*
 * Globals
 */
static EVP_CIPHER_CTX ctx;
static unsigned char  key[EVP_MAX_KEY_LENGTH];
static unsigned char  iv[EVP_MAX_IV_LENGTH];

#define KEY_LEN 16 //bytes

/*
 * select_random_key
 * 
 * len - key length in bytes
 */
static void
CS535_select_random_key(unsigned char *key, int len)
{
  int i;
  RAND_bytes(key,len);
  printf ("The key or iv len is: %d bytes\n",len);
  for (i = 0; i < len; i++) {
    printf ("%02X ", key[i]);
  }
  printf ("\n");

}

/*
 * setup_for_encrption
 */
static int
CS535_setup_for_encryption(unsigned  char * key, unsigned char *iv)
{

  EVP_EncryptInit(&ctx, EVP_aes_128_cbc(), key, iv);
  
  return 0;
}


/*
 * setup_for_decryption
 */
static int
CS535_setup_for_decryption(unsigned  char * key, unsigned char *iv)
{

  EVP_DecryptInit(&ctx, EVP_aes_128_cbc(), key, iv);
  
  return 0;
}

/*
 * main
 */

int main(void)
{
  printf("Hello CS535 Symmetric Cipher \n");
  printf ("--------------------------------\n");

  memset(key,0,EVP_MAX_KEY_LENGTH);
  memset(iv,0,EVP_MAX_KEY_LENGTH);

  printf ("Select a key\n");
  CS535_select_random_key(key,KEY_LEN);

  printf ("Select a IV\n");
  CS535_select_random_key(iv,KEY_LEN);


  printf ("Set up AES128CBC for encryption and decryption\n");
  CS535_setup_for_encryption(key, iv);
  CS535_setup_for_decryption(key,iv);

  printf ("The cipher ctx shows the required key length: %d bytes\n", EVP_CIPHER_CTX_key_length(&ctx));
  printf ("All Done!\n");
  printf ("--------------------------------\n");

  return;

}
