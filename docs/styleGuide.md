##Style Guide

#####We can use this space to publish our coding style as agreed upon between the devs



###Naming Standards
Modules should have lowercase names not including underscores or periods



###Import Standards

Imports of local modules (modules we are building )in same directory should always be done explicitly like:
   
    import cassandra

Check out this guide  http://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/

Specifically one thing I like from this is the explanation of import statements reproduced below. 
We should follow this set up. 


    #Very bad
        from modu import *
        x = sqrt(4)  # Is sqrt part of modu? A builtin? Defined above?
        
    #Better (still bad)
        from modu import sqrt
        x = sqrt(4)  # sqrt may be part of modu, if not redefined in between

    #Best
        import modu
        x = modu.sqrt(4)  # sqrt is visibly part of modu's namespace