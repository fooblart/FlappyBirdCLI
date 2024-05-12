#!/usr/bin/env python3
class main:
	def deathScreen(self):
		while True:
			for frame in ImageSequence.Iterator(Image.open('deathGif2.gif')):
				frame = frame.resize((100, 50), Image.NEAREST)
				pixels = frame.convert('RGB')
				width, height = frame.size
				print(f'Score: {self.green}{self.score}{self.end} Level: {self.green}{self.level}{self.end}')
				for h in range(height):
					for w in range(width):
						print('\x1b[38;2;' + ';'.join(list(map(str, pixels.getpixel((w, h))))) + 'm', end='█')
					print(self.end)
				time.sleep(frame.info['duration'] / 1000)
				self.clear(height + 1)
		exit()

	def exitScreen(self):
		print(self.green + '''
███████╗██╗  ██╗██╗████████╗███████╗██████╗     ██╗
██╔════╝╚██╗██╔╝██║╚══██╔══╝██╔════╝██╔══██╗    ██║
█████╗   ╚███╔╝ ██║   ██║   █████╗  ██║  ██║    ██║
██╔══╝   ██╔██╗ ██║   ██║   ██╔══╝  ██║  ██║    ╚═╝
███████╗██╔╝ ██╗██║   ██║   ███████╗██████╔╝    ██╗
╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝╚═════╝     ╚═╝''' + self.end)
		print(f'Score: {self.green}{self.score}{self.end} Level: {self.green}{self.level}{self.end}')
		exit()

	def clear(self, amount):
		print('\x1b[1A\x1b[2K' * amount, end='')

	def handleKeypress(self, key):
		match key:
			case keyboard.Key.space:
				self.frameArray[self.birdY][self.birdX] = self.sky
				self.birdY -= 5
			case keyboard.Key.esc:
				self.exitScreen()
			case keyboard.Key.ctrl:
				self.pause = not self.pause

	def initPipes(self):# create the pipes, should be no more than 10 per frame
		for i in range(self.pipeAmount):
			pipeHeight = random.randint(self.minPipeLength, round(self.frameHeight / 2)) #between 0 and 50
			self.pipes.append([
						i * self.pipeAmount + self.pipeAmount - 1,
						[self.topWallHeight + 1, pipeHeight], #1, 37ish
						[pipeHeight + self.pipeGap, self.bottomWallHeight - 1] #
					])
			#[x pos/ width, [top pipe start, top pipe end], [bottom pipe start, bottom pipe end]

	def draw(self):
		print(f'[FlappyBirdCLI] Level: {self.green}{self.level}{self.end} Score: {self.green}{self.score}{self.end} Distance: {self.green}{self.totalDistance}{self.end} Lives: ', end = self.red)
		for i in range(self.lives):
			print('💜', end = ' ')
		print(self.end)
		for row in self.frameArray:
			for pixel in row:
				print('\x1b[38;2;' + ';'.join(list(map(str, pixel[0]))) + 'm' + pixel[1] + self.end, end = '')
			print(self.end)
		self.clear(self.frameHeight + 1)

	def __init__(self):
		backgroundPixel = '██'
		if len(sys.argv) == 2:
			if sys.argv[1] == '--help':
				print('''
Jump: Space
Pause: Ctrl
Exit: Esc''')
				input('Press any Key to continue')


		wallColours = [[0, 255, 255], [0, 255, 0], [255, 0, 0], [255, 0, 255], [0, 0, 255]]
		wall = [[0, 255, 0], backgroundPixel]

		pipeColours = [[0, 255, 0], [0, 255, 255], [255, 0, 255], [0, 0, 255], [255, 0, 0]]
		pipe = [[0, 107, 11], backgroundPixel]

		skyColours = [[255, 0, 0], [255, 0, 255], [0, 0, 255], [0, 255, 255], [0, 255, 0]]
		self.sky = [[1, 201, 232], backgroundPixel]

		fps = 10
		self.end = '\x1b[0m'
		self.pause = False
		#TODO parse some of these as args once finised
		self.frameWidth = 100
		self.frameHeight = 50
		self.topWallHeight = 0
		self.bottomWallHeight = self.frameHeight
		self.pipeAmount = 10
		self.pipeGap = 15
		self.minPipeLength = 10
		self.pipes = []
		self.red = '\x1b[38;2;255;0;0m'
		self.green = '\033[38;2;0;255;0m'
		self.initPipes()
		bird = [[255, 255, 0], backgroundPixel]
		self.birdY = round(self.frameHeight / 2) #50
		self.birdX = round(self.frameWidth / 20) #5
		walls = [wall for _ in range(self.frameWidth)]
		self.levelChange = 2000
		self.score = 0
		self.lives = 3
		self.level = 0

		self.totalDistance = 0
		#DONE once score is high enough , give more lives, change colours, increase pipe gap, etc ..
		#TODO give medal based on score

		initialFrameArray = [[self.sky for _ in range(self.frameWidth)] for _ in range(self.frameHeight)]
		# for some reason naive method would mean that if we tried to update a certain value at certain index
		# i.e.: `self.frameArray[0][0] = self.sky` it would actually update everything in frameArray[0][*] as well and means the sub array [0][*] becomes uneditable

		for i in range(3):
			print(f'Starting game in {3 - i} seconds!')
			time.sleep(1)
			self.clear(1)

		try:
			with keyboard.Listener(on_press=self.handleKeypress) as listener:
				self.frameArray = initialFrameArray
				self.frameArray[self.topWallHeight] = walls
				self.frameArray[self.bottomWallHeight - 1] = walls
				while True:
					if not self.pause:
						for pipeData in self.pipes:
							if self.birdY >= pipeData[1][0] and self.birdY <= pipeData[1][1] and self.birdX == pipeData[0]:
								self.birdY = round(self.frameHeight / 2) #50
								self.lives -= 1
							if self.birdY >= pipeData[2][0] and self.birdY <= pipeData[2][1] and self.birdX == pipeData[0]:
								self.birdY = round(self.frameHeight / 2) #50
								self.lives -= 1

							for i in range(pipeData[1][0], pipeData[1][1]):
								self.frameArray[i][pipeData[0]] = pipe

							for i in range(pipeData[2][0], pipeData[2][1]): #bottom pipe
								self.frameArray[i][pipeData[0]] = pipe

						self.frameArray[self.birdY][self.birdX] = bird
						self.draw()

						for j in range(len(self.pipes)): #update/remove pipes add new pipes , paint over old pipes with self.sky colour
							topX, topY = self.pipes[j][1]

							bottomX, bottomY = self.pipes[j][2]#paint over top pipes
							for i in range(topX, topY):
								self.frameArray[i][self.pipes[j][0]] = self.sky

							for i in range(bottomX, bottomY):#paint over bottom pipes
								self.frameArray[i][self.pipes[j][0]] = self.sky

							if self.pipes[j][0] <= 0:# remove pipe if its position goes off the screen aka 0
								self.pipes.pop(j)
								pipeHeight = random.randint(self.minPipeLength, round(self.frameHeight / 2)) #between 0 and 50
								self.pipes.append([self.frameWidth - 1,
									[self.topWallHeight + 1, pipeHeight],
									[pipeHeight + self.pipeGap, self.bottomWallHeight - 1] #
								])
								continue

							if self.birdX == self.pipes[j][0]:
								self.score += 1
							if self.birdX <= self.pipes[j][0]:
								self.totalDistance += 1
								#level change code
								if self.totalDistance % self.levelChange == 0:
									if self.pipeGap >= 8:
										self.pipeGap -= 4

									newWallColour = wallColours[0]
									wallColours.append(wallColours.pop(wallColours.index(newWallColour)))
									wall = [newWallColour, backgroundPixel]

									newPipeColour = pipeColours[0]
									pipeColours.append(pipeColours.pop(pipeColours.index(newPipeColour)))
									pipe = [newPipeColour, backgroundPixel]

									newSkyColour = skyColours[0]
									skyColours.append(skyColours.pop(skyColours.index(newSkyColour)))
									self.sky = [newSkyColour, backgroundPixel]

									self.lives += 1
									self.level += 1
									fps += 1
								#colour changing things here

							self.pipes[j][0] -= 1

						self.frameArray[self.birdY][self.birdX] = self.sky
						self.birdY += 1

						if self.birdY >= self.frameHeight - 1 or self.birdY <= 1:
							self.birdY = round(self.frameHeight / 2)
							self.lives -= 1

						if self.lives <= 0:
							self.deathScreen()

					else:
						if input(self.end + 'Paused, resume [Y/N]? ').lower() in ['y', 'yes', '']:
							self.pause = False
							self.clear(1)
						else:
							self.exitScreen()
					time.sleep(1 / fps)
			listener.join()
		except KeyboardInterrupt:
			pass
		self.exitScreen()


if __name__ == '__main__':
	import random, time, sys
	from pynput import keyboard
	from PIL import Image, ImageSequence
	main()
