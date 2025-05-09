# mongodb-ola

rs.initiate({
_id: "configReplSet",
configsvr: true,
members: [{ _id: 0, host: "configsvr:27018" }]
})

rs.initiate({
_id: "shard1ReplSet",
members: [{ _id: 0, host: "shard1:27019" }]
})

rs.initiate({
_id: "shard2ReplSet",
members: [{ _id: 0, host: "shard2:27020" }]
})

sh.addShard("shard1ReplSet/shard1:27019")
sh.addShard("shard2ReplSet/shard2:27020")

sh.status()

