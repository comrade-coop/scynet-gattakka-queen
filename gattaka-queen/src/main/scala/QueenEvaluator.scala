package ai.scynet.queen

import com.obecto.gattakka.Evaluator
import com.obecto.gattakka.messages.eventbus.AddSubscriber
import com.obecto.gattakka.messages.population.{IntroducePopulation, PipelineFinishedEvent, RefreshPopulation}

class QueenEvaluator extends Evaluator {
  import com.obecto.gattakka.messages.evaluator._

  var populationSize = 0
  val requiredRatio = 0.9

  def tryRefresh() = {
    if (fitnesses.size >= populationSize * requiredRatio && populationSize > 0) {
      populationActor ! RefreshPopulation(false)
    }
  }

  override def customReceive = {

    case IntroducePopulation =>
      println("===== IntroducePopulation =====")
      originalReceive(IntroducePopulation)
      populationActor ! AddSubscriber(self, classOf[PipelineFinishedEvent])

    case PipelineFinishedEvent(totalSize, newComers) =>
      println("PipelineFinishedEvent")

      populationSize = totalSize
      tryRefresh()

    case x @ (_: SetFitness | _: RemoveFitness) =>
      originalReceive(x)
      tryRefresh()
  }
}
