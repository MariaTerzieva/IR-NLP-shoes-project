class SearchController < ApplicationController
  def search
    if params[:q].nil?
      @shoes = []
    else
      @shoes = Shoe.search params[:q]
    end
  end
end
