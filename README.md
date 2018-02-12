# PRMLstudy

PRMLの2章に出てきた確率分布の実装。PythonのPyQt5を使って確率分布のパラメータを変更して、分布の変化を確認できる。

## Install
リポジトリをクローンして、
  $ pip install -r requirements.txt

## Requirement
Python3.5
以下requirements.txt参照

## Usage
2.1.1 ベータ分布：
  $python BetaFunction.py

2.2.1 ディリクレ分布：
  $python DirichletDistribution.py
  
2.3.6 ガウス分布に対するベイズ推定
  $python GaussianDistribution.py
  
2.3.7 スチューデントのt分布
  $python tDistribution.py

2.3.8 フォン・ミーゼス分布
  $python vonMisesDistribution.py
 
2.5 ノンパラメトリック法
  $python NonParametric.py
  
(番外編) m勝n敗の時の勝率のベイズ推定　（参考-> <https://qiita.com/jyori112/items/80b21422b15753a1c5a4>）
  $python BayesianInference.py
