# Contributing

## Rough Notes

Using docker to test locally:

```sh
docker run -p 4000:4000 --rm --volume="$PWD:/srv/jekyll" -it jekyll/builder bash
```

And then, in the docker container:

```sh
gem install github-pages
jekyll serve
```
