<<<<<<< HEAD
##The Flow

- Find Peer Nodes
- Download a Block
  - Verify internal consistency of that Block
    - Previous Block Hash
    - TX Merkle Root
    - Other header stuff?
  - Search for relevant TXS of interest
    - edit metadata accordingly
=======
###TO DO
so many things

####short term
have a way to record the relationship between addresses as scores are added.  I want to see that
an address was a cousin, and a grandson, all together.  I want a verbal story for what the relationship
was.

save correlation records

create address vectors

compare address vectors between different addresses, use dot-product

  - dot product maps to markov-chain distance between addresses.  Find clusters this way

find a way to make this faster, think about how the TOP N for each generation are chosen (if we do
  subsegment branching)

####medium term

person objects composed of correlations to addresses

addresses inherit person correlations proportional to address-address vector-dot-products

how to run it all on a webserver

track bitcoin movement in addition to pure correlations, create new table for this
>>>>>>> 869b4dd92cbc7d1d040e42f060f60977991e9619
