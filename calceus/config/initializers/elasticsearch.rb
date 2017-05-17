Shoe.__elasticsearch__.client.indices.delete index: Shoe.index_name rescue nil

config = {
  host: "http://localhost:9200/",
  transport_options: {
    request: { timeout: 5 }
  },
}

if File.exists?("config/elasticsearch.yml")
  config.merge!(YAML.load_file("config/elasticsearch.yml").symbolize_keys)
end

Elasticsearch::Model.client = Elasticsearch::Client.new(config)

unless Shoe.__elasticsearch__.index_exists?
  Shoe.__elasticsearch__.client.indices.create index: Shoe.index_name,
   body: { settings: Shoe.settings.to_hash, mappings: Shoe.mappings.to_hash }
  Shoe.import
end