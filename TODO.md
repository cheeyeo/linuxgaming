# TODO

Stuff I would like to do.

## Move updates

Updates are currently run via cronjobs added to instances via AWS
ebextensions. This is shit for a few reasons:

  - if auto scaling kicks in then the cronjobs will run on 1*X servers.
  - any tom dick or harry can just to a get to the current URLs.

A better idea would be to move them to a lambda function or offload them
on to a worker instance of some kind.

## Fix feed config

I botched this by duplicating the website field so it would work with
the all sources page. I done this as I didnt know how to get the sub
fields within jinja2. This can be fixed with some investigating.

## Games schema

Need to thing of a good way to handle games, dont want to duplicate data
if not needed. This needs done before any other game source is added.

Not intested in the price side of things, loads of sites can already
provide you with this. I am thinking of something like this, some
sources dont have all the data needed so can just mix and match. HB for
example is shite.

Steam might be the best one to do first to populate the data.

"name": "gog",
"icon": "gog.png",
"type": "game",
"title": search_result['title'],
"publisher": search_result['publisher'],
"category": search_result['category'],
"url": "https://www.gog.com" + search_result['url'],
"date": dateutil.parser.parse(release_date)

title:
type: "game"
release_date:
publisher:
catagory:
gog:
  avaliable_date:
  url:
steam:
  avaliable_date:
  url:

## Steam API logic

Get all games
For each game
  get game information
  if linux platform
  save
  next

get all linux games in DB for steam
Get all games
For each game
  already in the DB list
    continue
  get game information
  if linux platform
  save
  next


## Add API

Would be nice to have api endpoints for different searches etc. This
would also allow better search on the site by using REST requests on
the main input search.

## Itch.io games

They do have a API but its really poor at this point. You can only
search by a query and cant limit by platform.

## Steam games

This should be easy to do.

## Humble Bundle games

Should be easy to do have already investigated. See the hb file in the
root folder for an example, output is poor though.

## Better searching

Current search method is just some js that searches already loaded table
contents, would like to add something better, see Add API.

