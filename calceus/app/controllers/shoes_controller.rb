class ShoesController < ApplicationController
  before_action :set_shoe, only: [:show, :edit, :update, :destroy]

  def index
    @shoes = Shoe.limit(10)
  end

  def show
    @similar_shoes = Shoe.more_like_this(@shoe).results.to_a
  end

  def new
    @shoe = Shoe.new
  end

  def edit
  end

  def update
    if @shoe.update(shoe_params)
      redirect_to @shoe, notice: 'Обувките бяха успешно обновени.'
    else
      render :edit
    end
  end

  def create
    @shoe = Shoe.new(shoe_params)

    if @shoe.save
      redirect_to @shoe, notice: 'Обувките бяха успешно създадени.'
    else
      render :new
    end
  end

  def destroy
    @shoe.destroy
    redirect_to shoes_url, notice: 'Обувките бяха успешно изтрити.'
  end

  private
    def set_shoe
      @shoe = Shoe.find(params[:id])
    end

    def shoe_params
      params.require(:shoe).permit(:title, :photo, :link, :price, :sizes, :colors, :gender, :sizes_list, :colors_list)
    end
end
