#TOREPLACE
#posfullname = entry's part of speech's full name
#poscode = part of speech's code
#lemma = entry's lemma
#gloss = entry's gloss
#formsandstems = entry's forms and stems
#audiobasicforms = list of audios for entry
#examplesentences = examplesentences
#wordfamily = wordfamily
from .htmlmaker import conj_call
def reducedentry_t(entry):
      return f'''
    <span class="main-entry-title">

      <span class="lemma"><a href="{entry.url}">noozhe-bizhiw</a></span>
      <span class="badge badge-oj" data-toggle="tooltip" data-placement="right" title="" data-original-title="{entry.pos.name}">
        {entry.pos.code}
      </span>

    </span>
    {entry.gloss}
    '''
def relatedwords(entry):
    return f'''
    <h3>Related Words</h3>
    <div class="stylized-text">{entry.relatedwords.name}</div>
    {''.join(reducedentry_t(rentry) for rentry in entry.relatedwords.entries)}
    '''

wordfamilychildren = ""
for child in entry.children:
    wordfamilychildren.append(f'''</span>a man</span><div class="indent"><span class="word-family-child "><span class="main-entry-title">
          {child.type}
          <span class="lemma"><a href="{child.url}">{child.lemma}</a></span>
          <span class="badge badge-oj" data-toggle="tooltip" data-placement="right" title="" data-original-title="{child.pos.full}">
            {child.pos.code}
          </span>''')

wordfamilytemplate = f'''<div class="word-family">
<span class="word-family-child highlight"><span class="main-entry-title">

      <span class="lemma"><a href="{entry.family.head.url}">inini</a></span>
      <span class="badge badge-oj" data-toggle="tooltip" data-placement="right" title="" data-original-title="{entry.family.head.pos.full}">
        {entry.family.head.pos.code}
      </span>
      {wordfamilychildren}

    </div></div>
    '''


entrytemplate = f'''
<div class="row content-container">
      <div class="col-md-9 col-sm-9 content">


<h3>
  <span class="lemma">{lemma}</span>
  <span class="badge badge-oj" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{posfullname}}">{{poscode}}</span>
    <a href="/speaker/rose-tainter" class="speaker-initials" data-toggle="modal" data-target="#voiceModal" data-remote="false">
        rg
      </a> <span class="badge badge-oj badge-audio-player">
      <div id="audio-player-113271" class="audio-player" data-file="https://s3.amazonaws.com/ojibwe-audio-transcoded/inini__na_sg__gp68049_2.flv" data-mobile-file="https://s3.amazonaws.com/ojibwe-audio-transcoded/inini__na_sg__gp68049_2.mp4">
        <span class="glyphicon glyphicon-volume-up glyphicon-audio-player"></span>
        Listen
      </div>
    </span>
</h3>

<p class="regions">
</p>

<p class="glosses">
 {gloss}
</p>


<p class="relations">



</p>



<p class="glossing">
  <br>
  <br>

    </p><p></p>
<p></p>

<p class="inflectional-forms"> {formsandstems}
</p>

<div class="panel panel-oj">
  <div class="panel-heading" role="tab" id="audioBasicFormsHeader">
    <h4 class="panel-title">
      <a class="" role="button" data-toggle="collapse" href="#audioBasicForms" aria-expanded="true" aria-controls="audioBasicForms">
        <span class="caret"></span>
        Audio for Basic Forms
      </a>
    </h4>
  </div>
  {audiobasicforms}
  </div>
</div>


  <p></p>

<div class="panel panel-oj">
  <div class="panel-heading" role="tab" id="sentenceExamplesHeader">
    <h4 class="panel-title">
      <a class="" role="button" data-toggle="collapse" href="#sentenceExamples" aria-expanded="true" aria-controls="sentenceExamples">
        <span class="caret"></span>
        Sentence Examples
      </a>
    </h4>
  </div>
  <div id="sentenceExamples" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="sentenceExamplesHeader" aria-expanded="true">
    {examplesentences}
    </span><br></td></tr>
      </tbody></table>
    </div>
  </div>
</div>







<div class="modal fade" id="voiceModal" tabindex="-1" role="dialog" aria-labelledby="voiceModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
    </div>
  </div>
</div>

      </div>
      <div class="col-md-3 col-sm-3 sidebar">
        <p>
  Created and maintained by the University of Minnesota's <a href="http://amin.umn.edu/">Department of American Indian Studies</a>,
  <a href="https://www.lib.umn.edu/">University Libraries</a>,
  <br>and editor John D. Nichols.
</p>

<h3>Word Family</h3>
{wordfamily}



<h3>Additional Resources</h3>
<p>
  Many of the words in the Ojibwe People's Dictionary have related resources. Click through to the full dictionary entry to hear audio recordings, see images, read documents and watch videos. Here's a key to resource icons.
  </p><ul class="list-unstyled">
    <li><span class="glyphicon glyphicon-volume-up"></span> Audio recordings</li>
    <li><span class="glyphicon glyphicon-camera"></span> Images</li>
    <li><span class="glyphicon glyphicon-facetime-video"></span> Video</li>
    <li><span class="glyphicon glyphicon-paperclip"></span> Documents</li>
  </ul>
<p></p>

<h3>Speakers &amp; Regions Key</h3>
<p>
Individual speakers and speakers from different regions use different words when speaking. Each audio recording is marked with the initials of the Ojibwe speaker. Click on a speaker's initials to <a href="/about/voices">go to the speaker's bio page</a>. If an Ojibwe word is particular to a certain region, it will be marked with a region code. Click on the region code to go to the <a href="/help/regions">Regions</a> page.
</p>

      </div>
    </div>
'''
