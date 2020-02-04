# Contributing
A more in-depth contribution guide is coming soon. Please hold tight! For the time being, if you'd like to submit new resources, please open an issue on the Github project page. Thank you!

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
