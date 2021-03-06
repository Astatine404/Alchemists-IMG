from django.shortcuts import render
from .forms import ImageForm
from .models import Image, Filters
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse

#from .utilities import pred
import os

# Create your views here.
def index(request):
	form = ImageForm()

	if request.method == 'POST':

		root = settings.MEDIA_ROOT
		myfile = request.FILES['myfile']

		vvid = Image()
		vvid.image = myfile
		vvid.save()

		vids = '/media/' + str(vvid.image)

		vidss = 'IMGfilter/' + vids
		picname = os.path.join(settings.BASE_DIR, vidss);

		os.system("sudo python2 Website/utilities/pred.py " + picname)

		with open(os.path.join(settings.BASE_DIR, "f.txt"), 'r') as f:
			num = f.read()

		num = num[1:]
		num = num[0:len(num)-1]

		num = num.split(',')

		fil = []
		for n in num:
			fil.append(Filters.objects.get(number=int(n)))
#		num = pred.fn(picname)
		# num = list(num)
		print(fil)

		max = fil[0].likes
		recc = fil[0].number
		for f in fil:
			if f.likes > max:
				max = f.likes
				recc = f.number

		return render(request, 'Website/index.html', {'form': form, 'vid': myfile, 'resu': vids, 'fil1': fil[0], 'fil2': fil[1], 'fil3': fil[2], 'recc': recc})

	else:
		return render(request, 'Website/index.html', {'form': form})


def addlike(request, name):
	fil = Filters.objects.get(name=name)

	fil.likes += 1
	fil.save()

	return HttpResponse(fil.likes)
#	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
