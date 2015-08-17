## selenium-parallel-python
### Runs selenium scripts in parallel on Crossbrowsertesting.com
#### Written in Python

Its done 2 different ways:

1. Multithreaded
	<pre><code>
		python multithreaded/parallel.py
	</code></pre>
2. Nose
	<pre><code>
		nosetests --processes=\<number_of_processes\> --where=nose
	</code></pre>
