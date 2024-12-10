from django.db import DataError, models
from accounts.models import PlayerProfile
from dotenv import load_dotenv
import os
import requests
# Create your models here.
class ItemImage(models.Model):
    image_url = models.URLField(null=True, blank=True)
    image_file = models.ImageField(null=True, blank=True, upload_to='item-images/')

    def save(self, *args, **kwargs) -> None:
        if self.image_url is None and self.image_file is None:
            raise DataError('image_url and image_file cannot both be null')
        super().save(*args, **kwargs)

    @property
    def image(self) -> str:
        if self.image_url is not None:
            print(self.image_file)
            return self.image_url
        else:
            return self.image_file.url

class Item(models.Model):
    price = models.DecimalField(verbose_name='Item price', default='0.00', decimal_places=2, max_digits=10, blank=False, null=False)
    name = models.TextField(verbose_name='Item name', default='Kroger item', blank=False, null=False)
    image = models.OneToOneField(ItemImage, on_delete=models.CASCADE, verbose_name='Item image')
    daily_item = models.BooleanField(verbose_name='Potential daily item', default=True, blank=False, null=False)
    used_as_daily = models.BooleanField(verbose_name="Used as daily item", default=False, blank=False, null=False)
    practice_item = models.BooleanField(verbose_name='Potential practice item', default=False, blank=False, null=False)
    def __str__(self) -> str:
        return f'{self.name}'

class CommonPuzzle(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, verbose_name='Puzzle item', blank=False, null=False)
    
    class Meta:
        abstract = True

class DailyPuzzle(CommonPuzzle):
    date = models.DateField(verbose_name='Date of daily puzzle', auto_now_add=True, blank=False, null=False)

    def __str__(self) -> str:
        return f'Daily Puzzle {self.date}'
    
class PracticePuzzle(CommonPuzzle):
    pass

class Guess(models.Model):
    owner = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, verbose_name='Owner of guess', blank=False, null=False)
    
    daily_puzzle = models.ForeignKey(DailyPuzzle, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Daily Puzzle')
    practice_puzzle = models.ForeignKey(PracticePuzzle, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Practice Puzzle')
    
    num_guesses = models.IntegerField(verbose_name='Number of guesses made', default=0, null=False, blank=False)
    
    correctly_guessed = models.BooleanField(verbose_name='Correctly guessed price', default=False, null=False, blank=False)
    
    guess_one = models.DecimalField(verbose_name='Guess 1', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_two = models.DecimalField(verbose_name='Guess 2', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_three = models.DecimalField(verbose_name='Guess 3', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_four = models.DecimalField(verbose_name='Guess 4', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_five = models.DecimalField(verbose_name='Guess 5', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    guess_six = models.DecimalField(verbose_name='Guess 6', max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    
    closeness_guess_one = models.CharField(verbose_name='Guess 1 closeness', max_length=20, default=None, null=True, blank=True)
    closeness_guess_two = models.CharField(verbose_name='Guess 2 closeness', max_length=20, default=None, null=True, blank=True)
    closeness_guess_three = models.CharField(verbose_name='Guess 3 closeness', max_length=20, default=None, null=True, blank=True)
    closeness_guess_four = models.CharField(verbose_name='Guess 4 closeness', max_length=20, default=None, null=True, blank=True)
    closeness_guess_five = models.CharField(verbose_name='Guess 5 closeness', max_length=20, default=None, null=True, blank=True)
    closeness_guess_six = models.CharField(verbose_name='Guess 6 closeness', max_length=20, default=None, null=True, blank=True)
    
    def __str__(self) -> str:
        if self.daily_puzzle:
            return f'{self.owner.username}\'s {self.daily_puzzle.date} daily puzzle guess'
        else:
            return f'{self.owner.username}\'s practice puzzle guess'
class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Time of comment written", blank=False, null=False)
    user = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(blank=True, null=True, verbose_name='Comment image')
    puzzle = models.ForeignKey(DailyPuzzle, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Puzzle where comment is written')
    message = models.TextField(blank=False, null=False, default='')
    
    def __str__(self) -> str:
        return f'{self.user}\'s comment at {self.timestamp}'
    
def get_items():
    '''Gets 150 daily items and 150 practice items for use with the daily and practice puzzles'''
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    print(API_KEY)
    url = "https://api.kroger.com/v1/products" # get kroger items in the cincinatii ohio krogers specifically
    for i in range(6): # you can only go up to 50 per search, up to at most 300 items, so increment 50 each time
        res = requests.get(url=url, headers={"Content-Type": "application/json", "Authorization": "Bearer " + API_KEY}, params={"filter.locationId": "01400390", "filter.limit": 50, "filter.start": 50 * i, "filter.term": "Kroger"})
        res = res.json()
        res_length = len(res['data'])
        # creates daily items
        print("Creating Daily Items")
        for index in range(int(res_length / 2)):
            try:
                images = res['data'][index]['images']
                i = 0
                for image in images:
                    if image['perspective'] == 'front':
                        break
                    i+=1
                item_name = res['data'][index]['description']
                item_price = res['data'][index]['items'][0]['price']['regular']
                image = ItemImage.objects.create(image_url=res['data'][index]['images'][i]['sizes'][1]['url'])
                Item.objects.create(image=image, name=item_name, daily_item=True, price=item_price)
            except KeyError:
                # some items might not have prices or anything
                print(f"Skipped")
        # creates practice items
        print("Creating practice items")
        for index in range(int(res_length / 2)):
            try:
                images = res['data'][index + int(res_length / 2)]['images']
                i = 0
                for image in images:
                    if image['perspective'] == 'front':
                        break
                    i+=1
                item_name = res['data'][index + int(res_length / 2)]['description']
                item_price = res['data'][index + int(res_length / 2)]['items'][0]['price']['regular']
                image = ItemImage.objects.create(image_url=res['data'][index + int(res_length / 2)]['images'][i]['sizes'][1]['url'])
                Item.objects.create(image=image, name=item_name, daily_item=False, practice_item=True, price=item_price)
            except:
                # some items might not have prices or anything
                print(f"Skipped")
                
def create_practice_puzzles():
    # all items marked as potential practice puzzle items will be created
    potential_practice_puzzles = Item.objects.filter(daily_item=False)
    practice_puzzles = PracticePuzzle.objects.all()
    for practice_puzzle in practice_puzzles:
        potential_practice_puzzles.exclude(name=practice_puzzle.item.name) # chose a random field, but any field in the item is fine
    # create practice puzzles
    for item in potential_practice_puzzles:
        PracticePuzzle.objects.create(item=item)