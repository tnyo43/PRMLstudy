# PRMLstudy

PRMLの2章に出てきた確率分布の実装。PythonのPyQt5を使って確率分布のパラメータを変更して、分布の変化を確認できる。

## Install
リポジトリをクローンして、  
```shell
  $ pip install -r requirements.txt
```
## Requirement
Python3.5  
以下requirements.txt参照

## Usage
2.1.1 ベータ分布：
```shell
$python BetaFunction.py
```
2.2.1 ディリクレ分布：  
```shell
$python DirichletDistribution.py
```
2.3.6 ガウス分布に対するベイズ推定 
```shell
$python GaussianDistribution.py
```
2.3.7 スチューデントのt分布  
```shell
$python tDistribution.py
```
2.3.8 フォン・ミーゼス分布  
```shell
$python vonMisesDistribution.py
``` 
2.5 ノンパラメトリック法  
```shell
$python NonParametric.py
```
  
(番外編) m勝n敗の時の勝率のベイズ推定　（参考-> <https://qiita.com/jyori112/items/80b21422b15753a1c5a4>)
```shell
$python BayesianInference.py
```
