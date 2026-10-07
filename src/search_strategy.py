import random

starBucket = [
    "stars:1000..1249",
    "stars:1250..1499",
    "stars:1500..1999",
    "stars:2000..2499",
    "stars:2500..2999",
    "stars:3000..3999",
    "stars:4000..4999",
    "stars:5000..6999",
    "stars:7000..9999",
    "stars:10000..14999",
    "stars:15000..24999",
    "stars:25000..49999",
    "stars:50000..99999",
    "stars:>=100000",
]

def buildSearchQueries()->list[str]:
    buckets = starBucket.copy()
    random.shuffle(buckets)

    queries = []

    for bucket in buckets:
        queries.append(f"{bucket} fork:false archived:false")

    return queries
