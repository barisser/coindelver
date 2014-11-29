##CoinDelve

###Deanonymize the network
  - ####Scrape data off the web wherever possible.
    - Pull identity from known sources
  - ####Track correlations between addresses
    - Correlations move upwards and downwards through time.  They diminish exponentially.  Trace contributions are deleted to control scaleability.  Correlations extend between addresses, even without direct bitcoin transmission.
  - ####Monitor the movement of Bitcoins
    - Works similar to correlations, except vector contributions extend only backwards through time.  They also must be composed of bitcoin-for-bitcoin, not general correlations.
  - ####Identify laundered Bitcoin as such.



##Implementation
###Concepts
####Correlation
  - Addresses are correlated in many way.  If we've both sent BTC to the same address, we should be correlated.  If we both received bitcoin from the same grandfather address, we should be correlated.  

####Bitcoin Source
  - Where have these bitcoins come from?  Which addresses hands have they passed through?
    - This is captured as the bitcoin_id.  Each output maps to one bitcoin_id.  Each Bitcoin_id maps to multiple contributing bitcoin_ids.  
      - For one-to-one, the Bitcoin ID is the same, since the money is the same
      - For one-to-multiple, the Bitcoin ID is the same, since the source for all is the same.
      - For many in to one out, a new Bitcoin ID is generated.  It has the Bitcoin_IDs of its parents (labelled as parents).  If all parents are known to come from addresses with the same person_id, they become a single Bitcoin ID.  
      - For any given Bitcoin_ID, it comes with a vector of contributions from previous Bitcoin_IDs, which make up the basis vectors.  If too many Bitcoin_IDS accumulate, some are deleted.  Perhaps a max of 16 or 32...  This should be on another table.

      - Bitcoin_IDs should be merged whenever possible.  The same goes for person_ids.  
