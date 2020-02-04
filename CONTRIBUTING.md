# Contributing
A more in-depth contribution guide is coming soon. Please hold tight!

## Rough Notes

Using docker to test locally:

```sh
docker run -p 4000:4000 --name jekyll --volume="$PWD:/srv/jekyll" -it jekyll/jekyll bash
```

And then, in the docker container:

```sh
gem install github-pages
jekyll serve
```
