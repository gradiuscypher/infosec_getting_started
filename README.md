Using docker to test locally:
```
docker run -p 4000:4000 --rm --volume="$PWD:/srv/jekyll" -it jekyll/builder bash
```

And then, in the docker container:
```
gem install github-pages
jekyll serve
```