
/* 
 * sample code only!
 */

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


#define KEY_LEN 16 //bytes


/*
 * select_random_key
 * 
 * len - key length in bytes
 */

static void
CS535_select_random_key(unsigned char *key, int len)
{
  
  RAND_bytes(key,len);

}

/*
 * select_random_iv
 * 
 * len - iv length in bytes
 */

static void
CS535_select_random_iv(unsigned char *iv, int len)
{
  
  RAND_bytes(iv,len);

}

/*
 * setup_for_encrption
 */
static int
CS535_setup_for_encryption(unsigned  char * key, unsigned char *iv)
{

  EVP_EncryptInit_ex(&ctx, EVP_aes_128_cbc(), NULL, key, iv);

}


/*
 * setup_for_decryption
 */
static int
CS535_setup_for_decryption(unsigned  char * key, unsigned char *iv)
{

  EVP_DecryptInit_ex(&ctx, EVP_aes_128_cbc(), NULL, key, iv);

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

  CS535_setup_for_encryption(key, iv);

  EVP_EncryptUpdate(&ctx, enbuf,enlen, data, datalen);
 
  EVP_EncryptFinal_ex(&ctx, enbuf+(*enlen), &tmplen)

  *enlen += tmplen;

}

/*
 * CS535_decrypt
 */
static int
CS535_decrypt(char* data, int datalen, char *debuf, int *delen)
{


  int tmplen = 0;

  CS535_setup_for_decryption(key,iv);

  EVP_DecryptUpdate(&ctx, debuf, delen, data, datalen);

  EVP_DecryptFinal_ex(&ctx, debuf, &tmplen)

  *delen += tmplen;
}

/*****************************************
 * main
 ****************************************/

int main(void)
{

  char data[] = " Hello CS535B! ";


  CS535_select_random_key(key,KEY_LEN);


  CS535_select_random_iv(iv,KEY_LEN);

    

  CS535_encrypt(data, strlen(data), endata, &enlen)

 CS535_decrypt(endata,enlen, dedata, &delen) 
 



}
