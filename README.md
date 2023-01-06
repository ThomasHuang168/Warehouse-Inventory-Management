# Warehouse-Inventory-Management
a python script that manage Inventory in a warehouse

## Update
20230106 gui print labels

## Design consideration
- print a A4 sheet of qr-code, barcode and name label
- manage location with google sheet and pandas
  - how large can a google sheet be?
  - attribute and status management [each should link to a folder]
    - instances
    - classes
    - boxes [a special instance: NOT-for-sale]
    - locations [also a kind of ]
  - how to unqiue ID code for 
    - instances
    - classes
      - redundancy?
      - human verifiable?
        - know the catorgory by reading code
        - know the time of the record created
      - scalable? [this is the difficult one]
      - should it depend on time
- how to synchronzie in between Google and computers
  - limitation of google services
  - only one device is updating the database in any time interval
    - how small is one time interval

## implementation and testing stages
### Feedback from Mary stage
-   simple pandas manipulation
    -   one table for book instances map to box id
    -   box table link to [google drive] folder [path/link] inside which the picture of box is included and show its location
    -   one simple GUI to for add books, boxs, put books into boxes and remove books. 
    -   one simple labels text labels in three different formats barcode, qr-code and text.