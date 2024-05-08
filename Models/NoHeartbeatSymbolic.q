//This file was generated from (Academic) UPPAAL 5.0.0 (rev. 714BA9DB36F49691), 2023-06-21

*/
A[] not deadlock

/*

*/
E<> Server0.Reset

/*

*/
E<> Client0.Reset

/*

*/
E<> Client0.ClientHelloCookie imply Server0.SentCookies

/*

*/
A[] Server0.ServerHello imply Server0.SentCookies

/*