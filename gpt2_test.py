import gpt_2_simple as gpt2

model_name = '117M'

# gpt2.download_gpt2(model_name=model_name)

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              'hoyatitles.txt',
              model_name=model_name,
              steps=1000,
              save_every=200,
              sample_every=25)

prefix = 'neural'

print("Generating...")
text = gpt2.generate(sess,
              length=40,
              temperature=0.7,
              prefix=prefix,
              nsamples=1,
              batch_size=1,
              return_as_list=True
             )

print("Done!")
t = text[0].title()
t = t.replace('<|Startoftext|>', '').replace('\n', '') # remove extraneous stuff
t = t[:t.index('<|Endoftext|>')] # only get one title
print(t)
