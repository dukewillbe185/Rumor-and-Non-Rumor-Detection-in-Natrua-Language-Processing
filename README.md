# Rumor-and-Non-Rumor-Detection-in-Natrua-Language-Processing

This project can be divided into 2 parts: 
                      1)Crawling the data, which are tweets from Tweeiter API via tweepy2.0, and the documents are stored in Json files.
                      2)Building model and processing the pre-processing data step, and then try different models.
                      
In this project, I've tried tf-idf + traditional models like SVM, Random Forest, Logistic Regression, and ave F1 is about 70.

Compared with the most advanced BERTWEET model(93.56), they perfomr a bit poor.

For BERTWEET model, I did follwing things:

  1)Clip
  Since a lot of GELU or SoftMax activation are applied into the BERT variant model, it is reasonble that the gradient explosion appears easily.To deal with this, I added gradient clip
    
  2)Unweighted Class
  The proportion of rumor labled data and unrumor labeld data is 4:1, which is obviously imbalanced. To deal with it, I applied unweighed in CrossEntropy loss function, to penalise the wrong predictions in rumor data.
  
  Optimiser is Adam, the current most popular one.
  
  You can read criteria in project.pdf, and methods in models document.
    
    
                  
