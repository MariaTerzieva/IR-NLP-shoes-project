class Shoe
  include Mongoid::Document
  include Elasticsearch::Model
  include Elasticsearch::Model::Callbacks

  field :title
  field :photo
  field :link
  field :price
  field :gender
  field :sizes, type: Array, default: []
  field :colors, type: Array, default: []

  validates_presence_of :title
  validates_presence_of :photo
  validates_presence_of :link
  validates_presence_of :price
  validates_presence_of :gender
  validates_presence_of :sizes
  validates_presence_of :colors

  settings index: {
    number_of_shards: 1, 
    number_of_replicas: 0,
    analysis: {
      filter: {
        my_stemmer: {
          type: 'stemmer',
          language: 'bulgarian'
        },
        my_soundex: {
          type: 'phonetic',
          encoder: 'doublemetaphone',
          replace: false
        }
      },
      analyzer: {
        myAnalyzer: {
          type: 'custom',
          tokenizer: 'standard',
          filter: ['standard', 'lowercase', 'my_soundex', 'my_stemmer']
        }
      }
    }
  } do
    mappings dynamic: 'false' do
      indexes :title, analyzer: 'myAnalyzer'
      indexes :colors, analyzer: 'myAnalyzer'
      indexes :gender, analyzer: 'myAnalyzer'
      indexes :price
      indexes :photo
      indexes :link
      indexes :sizes
    end
  end

  def sizes_list=(arg)
    self.sizes = arg.split(',').map(&:strip)
  end

  def sizes_list
    self.sizes.join(', ')
  end

  def colors_list=(arg)
    self.colors = arg.split(',').map(&:strip)
  end

  def colors_list
    self.colors.join(', ').downcase
  end

  def as_indexed_json(options={})
    as_json(except: [:id, :_id])
  end

  def self.more_like_this(shoe)
    black_list = ['спортни', 'обувки', 'ботуши', 'туристически', 'джапанки',
            'апрески', 'футболни', 'платформа', 'сандали', 'дамски', 'кецове',
            'маратонки', 'зимни', 'чехли', 'мъжки', 'балеринки', 'black', 'white',
            'red', 'blue', 'grey']

    filtered_title = shoe.title.mb_chars.downcase.to_s.gsub(/( | \w)(\d)+/, "")
    black_list.each do |word|
      filtered_title = filtered_title.gsub(word, "")
    end

    filtered_title = filtered_title.split(' ').uniq
    filtered_title.shift

    if filtered_title.size <= 2
      minimum_should_match = "100%"
    else
      minimum_should_match = "75%"
    end

    filtered_title = filtered_title.to_s

    __elasticsearch__.search(
      {
        query: {
          bool: {
            filter: {
              match: {
                title: {
                  query: filtered_title,
                  minimum_should_match: minimum_should_match
                }
              }
            },
            should: [
              {
                more_like_this: {
                  fields: ['colors'],
                  docs: [
                    {
                      _index: 'shoes',
                      _type: 'shoe',
                      _id: shoe.id.to_s
                    }
                  ],
                  ids: [shoe.id.to_s]
                }
              },
              {
                more_like_this: {
                  fields: ['gender'],
                  docs: [
                    {
                      _index: 'shoes',
                      _type: 'shoe',
                      _id: shoe.id.to_s
                    }
                  ],
                  ids: [shoe.id.to_s]
                }
              }
            ],
            minimum_should_match: 2
          }
        }
      }
    )
  end

  def self.search(query)
    __elasticsearch__.search(
      {
        query: {
          multi_match: {
            query: query,
            fields: ['title', 'gender', 'colors', 'sizes', 'price'],
            tie_breaker: 0.5,
            analyzer: 'myAnalyzer'
          }
        }
      }
    )
  end
end
