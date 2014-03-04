#include <stdio.h>
#include <stdlib.h>

#include <openssl/evp.h>
#include <openssl/rand.h>


static void
CS535_select_random_key(char *key, int n)
{
  int i;
  RAND_bytes(key, n);
  printf ("The key is: \n");
  for (i = 0; i < n; i++) {
    printf ("%02X\n", key[i]);
  }
  printf ("\n");

}


int main(void)
{
  printf(" Hello CS535 Symmetric Cipher \n");

  return;

}
