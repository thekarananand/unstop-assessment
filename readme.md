# Unstop Assessment

Deployed here : [https://unstop-assessment-green.vercel.app/](https://unstop-assessment-green.vercel.app/)

![Application Layout](./media/p1.png)


## Database Structure
![DB Layout](./media/p2.png)

Leveraged **Cloud Firestore**, a NoSQL database for storing two arrays: 

 - `current_state` 
 - `initial_state`

For context, `state` varible represents the number of vacant seat in a given row, corrosponding to the index.