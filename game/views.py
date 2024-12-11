from django.shortcuts import render, redirect
from datetime import date
from .models import Guess, DailyPuzzle, Comment, PlayerProfile, PracticePuzzle, Item
from .forms import GameForm, CommentForm
from decimal import Decimal
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.urls import reverse
import random


# Create your views here.
def home(request):
    """home view"""
    num_to_string = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    # Get a daily puzzle
    daily_puzzle = get_daily_puzzle()
    template_name = "game/home.html"
    game_form = GameForm()
    submission_validation = uuid.uuid4()  # idempotency key
    context = {
        "item_name": daily_puzzle.item.name,
        "item_image": daily_puzzle.item.image.image,
        "item_price": daily_puzzle.item.price,
        "form": game_form,
        "closeness": None,
        "guess_price": None,
        "guess": [],
        "date": date.today(),
        "submission_validation": submission_validation,
        "logged_in": False,
        "comments": None,
        "show_comment_link": False,
        "random_puzzle_pk": None,
    }
    if request.POST:
        form = GameForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            if request.session.get("idempotency_key") == request.POST.get(
                "submission_validation"
            ):  # double submission
                print("double submission")
                return redirect("home")
            request.session["idempotency_key"] = request.POST.get(
                "submission_validation"
            )  # set the session idempotency key to the form's key so that the new submission will go through, only when the keys are the same will it count as a double submission (prevents refreshes counting as posts)
            item_price = Decimal(daily_puzzle.item.price)
            guess_price = Decimal(data["guess"])
            closeness = closeness_in_price(item_price, guess_price)
            context["closeness"] = closeness
            context["guess_price"] = guess_price
            print(closeness)
            if request.user.is_authenticated:
                try:
                    guess = Guess.objects.get(owner=request.user.playerprofile, daily_puzzle=daily_puzzle)
                    num_guesses = guess.num_guesses
                    # to prevent anyone posting a POST request with a guess even though they had a correct answer (prevents bypassing the submit button being disabled)
                    if not guess.correctly_guessed and num_guesses < 6:
                        setattr(guess, "num_guesses", num_guesses + 1)
                        setattr(
                            guess,
                            "guess_" + num_to_string[num_guesses + 1],
                            guess_price,
                        )
                        print(closeness)
                        if closeness == "exact":
                            setattr(guess, "correctly_guessed", True)
                        setattr(
                            guess,
                            "closeness_guess_" + num_to_string[num_guesses + 1],
                            closeness,
                        )
                        guess.save()
                except Guess.DoesNotExist:
                    # no guess object found, so create one and add the guess to this
                    guess = Guess.objects.create(
                        owner=request.user.playerprofile,
                        daily_puzzle=daily_puzzle,
                        num_guesses=1,
                        guess_one=guess_price,
                        closeness_guess_one=closeness,
                    )
        else:
            print("Not valid form")
            return redirect("home")

    # if the user is authenticated, return the guesses model fields instead of the actual guess
    if request.user.is_authenticated:
        context["logged_in"] = True
        try:
            # iterate through all the guess fields and attach it to the context
            guess = Guess.objects.get(owner=request.user.playerprofile, daily_puzzle=daily_puzzle)
            num_guesses = guess.num_guesses
            guess_object = guess.guess_one
            closeness_object = guess.closeness_guess_one
            guesses = [
                "guess_one",
                "guess_two",
                "guess_three",
                "guess_four",
                "guess_five",
                "guess_six",
            ]
            for index, guess_name in enumerate(guesses):
                guess_object = getattr(guess, guess_name)
                closeness_object = getattr(
                    guess, "closeness_guess_" + num_to_string[index + 1]
                )
                if guess_object is None and closeness_object is None:
                    break
                if guess == "guess_one":
                    context["guess"] = [
                        {"guess": guess_object, "closeness": closeness_object}
                    ]
                else:
                    context["guess"].append(
                        {"guess": guess_object, "closeness": closeness_object}
                    )
            print(context["guess"])
            # if the game is over, show comments
            if (
                not guess.correctly_guessed and num_guesses >= 6
            ) or guess.correctly_guessed:
                context["comments"] = Comment.objects.filter(puzzle=daily_puzzle)
                # passes a random puzzle in for authenticated users ONLY
            context["random_puzzle_pk"] = get_random_puzzle(request)
        except Guess.DoesNotExist:
            Guess.objects.create(
                owner=request.user.playerprofile,
                daily_puzzle=daily_puzzle,
            )

            # for the template
    if context["comments"] is not None:
        context["show_comment_link"] = True

    return render(request, template_name, context)


def get_daily_puzzle():
    """gets a daily puzzle from items thats marked as daily_item"""
    todays_date = date.today()
    puzzles = DailyPuzzle.objects.filter(date=todays_date)
    # if no such puzzle exists (typically because its a new day, create one)
    if len(puzzles) == 0:
        potential_daily_puzzles = Item.objects.exclude(
            used_as_daily=True, daily_item=True
        )
        item = random.choice(potential_daily_puzzles)
        # sets the item's used_as_daily to true to remove it from selection on the next daily puzzle
        setattr(item, "used_as_daily", True)
        daily = DailyPuzzle.objects.create(item=item)
        return daily
    else:
        return puzzles[0]


def closeness_in_price(item_price, guess_price):
    """checks how close the guess is to the actual price"""
    closeness = ""  # guess is within 10% of the item price
    close_to_item_price_percentage = Decimal(0.25)
    lower_bound = item_price * Decimal(0.9)
    upper_bound = item_price * Decimal(1.1)
    if lower_bound <= guess_price <= upper_bound:
        return "exact"

    # guaranteed to be lower or greater than 10% of the item price
    if guess_price < lower_bound:
        closeness = "lower "
    else:
        closeness = "upper "

    if abs(item_price - guess_price) / item_price <= close_to_item_price_percentage:
        closeness += "close"
    else:
        closeness += "far"

    return closeness


class CreateCommentView(LoginRequiredMixin, CreateView):
    """Creates comments"""

    model = Comment
    form_class = CommentForm
    template_name = "game/create_comment.html"

    def get_object(self, queryset=...):
        # gets the player that requested this to create the comment
        return PlayerProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        # gets the daily puzzle (only puzzle with comments) and attaches a comment to it along with the user
        daily_puzzle = get_daily_puzzle()

        user = PlayerProfile.objects.get(user=self.request.user)
        form.instance.puzzle = daily_puzzle
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("home")


class RandomPracticePuzzleView(LoginRequiredMixin, DetailView):
    """gets a random puzzle based on the user's puzzle submissions"""

    model = PracticePuzzle
    template_name = "game/random.html"
    context_object_name = "puzzle"

    # gets the form associated with it and attach it, the guess associated with it and attach it, and the idempotency key, just like in the home view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("get_context_data")
        print("PK = ")
        print(self.kwargs['pk'])
        try:
            guess = Guess.objects.get(owner=self.request.user.playerprofile, practice_puzzle=PracticePuzzle.objects.get(pk=self.kwargs['pk']))
            print(guess.guess_one)
            context["guesses"] = guess
        except Guess.DoesNotExist:
            # creates a guess object and attaches this puzzle to it
            puzzle = PracticePuzzle.objects.get(
                pk=self.kwargs['pk']
            )  # guaranteed to exist since we're at this view
            Guess.objects.create(
                owner=self.request.user.playerprofile,
                practice_puzzle=puzzle,
                num_guesses=0,
            )
        context['submission_validation'] = uuid.uuid4()
        context['form'] = GameForm()
        print(context['form'])
        return context
    # virutally the same as the home view logic
    def post(self, request, *args, **kwargs):
        num_to_string = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
        form = GameForm(request.POST)
        print(self.kwargs['pk'])
        if form.is_valid():
            data = form.cleaned_data
            if request.session.get("idempotency_key") == request.POST.get(
                "submission_validation"
            ):  # double submission
                print("double submission")
                return redirect("home")
            request.session["idempotency_key"] = request.POST.get(
                "submission_validation"
            )
            item_price = Decimal(PracticePuzzle.objects.get(pk=self.kwargs['pk']).item.price)
            guess_price = Decimal(data["guess"])
            closeness = closeness_in_price(item_price, guess_price)
            try:
                    guess = Guess.objects.get(owner=request.user.playerprofile, practice_puzzle=PracticePuzzle.objects.get(pk=self.kwargs['pk']))
                    num_guesses = guess.num_guesses
                    # to prevent anyone posting a POST request with a guess even though they had a correct answer (prevents bypassing the submit button being disabled)
                    if not guess.correctly_guessed and num_guesses < 6:
                        setattr(guess, "num_guesses", num_guesses + 1)
                        setattr(
                            guess,
                            "guess_" + num_to_string[num_guesses + 1],
                            guess_price,
                        )
                        print(closeness)
                        if closeness == "exact":
                            setattr(guess, "correctly_guessed", True)
                        setattr(
                            guess,
                            "closeness_guess_" + num_to_string[num_guesses + 1],
                            closeness,
                        )
                        guess.save()
            except Guess.DoesNotExist:
                    # no guess object found, so create one and add the guess to this
                    guess = Guess.objects.create(
                        owner=request.user.playerprofile,
                        daily_puzzle=PracticePuzzle.objects.get(pk=self.kwargs['pk']),
                        num_guesses=1,
                        guess_one=guess_price,
                        closeness_guess_one=closeness,
                    )
        
            self.object = self.get_object()
            context = self.get_context_data(**kwargs)


        
                    
        return self.render_to_response(context=context)
            
    # def form_valid(self, form):
    #     num_to_string = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    #     if self.request.POST:
    #         guess = Guess.objects.get(owner=self.request.user.playerprofile)
    #         num_guesses = guess.num_guesses
    #         form = GameForm(self.request.POST)
    #         data = form.cleaned_data
    #         item_price = Decimal(PracticePuzzle.objects.get(pk=self.pk).item.price)
    #         guess_price = Decimal(data['guess'])
    #         closeness = closeness_in_price(item_price, guess_price)
    #         if self.request.session.get("idempotency_key") == self.request.POST.get(
    #             "submission_validation"
    #         ):  # double submission
    #             print("double submission")
    #             return redirect("home")
    #         self.request.session["idempotency_key"] = self.request.POST.get(
    #             "submission_validation"
    #         )
    #         if not guess.correctly_guessed and num_guesses < 6:
    #             setattr(guess, "num_guesses", num_guesses + 1)
    #             setattr(
    #                 guess,
    #                 "guess_" + num_to_string[num_guesses + 1],
    #                 guess_price,
    #             )
    #             print(closeness)
    #             if closeness == "exact":
    #                 setattr(guess, "correctly_guessed", True)
    #             setattr(
    #                 guess,
    #                 "closeness_guess_" + num_to_string[num_guesses + 1],
    #                 closeness,
    #             )
    #             guess.save()
    #     return super().form_valid(form)


def get_random_puzzle(request):
    user = request.user
    potential_practice_puzzles = PracticePuzzle.objects.all()
    guesses = Guess.objects.filter(owner=user.playerprofile, daily_puzzle=None)
    print(guesses)
    if guesses is not None:
        print(True)
        for guess in guesses:
            potential_practice_puzzles.exclude(item=guess.practice_puzzle.item)
    return random.choice(potential_practice_puzzles).pk
