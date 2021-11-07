# PDroid

PDroid is a static analysis tool that helps understand the privacy practices of Android application. PDroid has a CLI that allows you to statically analyze an Android application. 

_Updated README coming soon._

## Citation

PDroid is a tool that is part of an ongoing project at the PERC-Lab. If you use PDroid, please cite it.

```
@inproceedings{jain2021prigen,
  title={PriGen: Towards Automated Translation of Android Applications’ Code to Privacy Captions},
  author={Jain, Vijayanta and Gupta, Sanonda Datta and Ghanavati, Sepideh and Peddinti, Sai Teja},
  booktitle={International Conference on Research Challenges in Information Science},
  pages={142--151},
  year={2021},
  organization={Springer}
}
```

## Setup
1. Clone repo in same directory where all apks are stored
2. cd into PDroid
3. Create virtual environment and make sure all dependancies are installed
4. Move getPerms.py into original folder with the apks
5. cd back to original folder and run script

### Commands
`git clone https://github.com/sajidrahman/PDroid.git`
`cd PDroid`
install requirements
`mv getPerms.py .. && cd ..`
`python3 getPerms.py`
