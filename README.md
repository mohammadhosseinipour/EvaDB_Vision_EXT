# EvaDB_Vision_EXT
Some computer vision extensions to EvaDB and an example of using them instead of training an ML model to solve it.
## Instructions:
  1. ADD `blob_detector.py`, `grayscale.py`, `high_pass.py`, `moment.py`, and `threshold.py` to the `.../evadb/functions/ndarray` folder of your evadb library location.
  2. The `Concrete_detector.py` will process every image in [Image](https://github.com/mohammadhosseinipour/EvaDB_Vision_EXT/tree/main/Images) folder with `.jpeg` format!
  3. That's it!


  
## How to run the example?
  1. Run `Concrete_detector.py` in your terminal(make sure Images folder is in the same place!).
  ```bat
  python3 Concrete_detector.py
  ```
  2. Enter the path where the evadb root library is there.



### Result Examples:
![2](./results/2.png)
![3](./results/3.png)  
